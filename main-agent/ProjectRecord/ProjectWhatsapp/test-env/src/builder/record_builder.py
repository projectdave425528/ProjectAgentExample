"""Transaction Record Builder — main integration logic.

Combines matcher, extractor, and status_resolver to produce
a complete list of TransactionRecord from messages and images.
"""
import json
import logging
from decimal import Decimal

from src.builder.matcher import (
    match_images_to_messages,
    MatchResult,
    MatchedPair,
)
from src.builder.extractor import (
    extract_from_matched_pair,
    group_by_time_window,
    ExtractionResult,
)
from src.builder.status_resolver import resolve_payment_status
from src.models.message import ParsedMessage
from src.models.image_result import ImageAnalysisResult
from src.models.transaction import TransactionRecord

logger = logging.getLogger(__name__)

REVIEW_THRESHOLD: float = 0.6


def build_records(
    messages: list[ParsedMessage],
    image_results: list[ImageAnalysisResult],
) -> list[TransactionRecord]:
    """Build TransactionRecord list from messages and images.

    Flow:
    1. Match images to messages
    2. Extract info from each matched pair
    3. Group by time window
    4. Resolve payment status per group
    5. Assemble TransactionRecord

    Args:
        messages: Parsed WhatsApp messages.
        image_results: Image analysis results.

    Returns:
        List of assembled TransactionRecord.
    """
    match_result = match_images_to_messages(
        messages, image_results
    )
    if not match_result.matched_pairs:
        return _build_unmatched_records(match_result)

    return _build_from_matched(match_result)


def records_to_json(records: list[TransactionRecord]) -> str:
    """Serialize TransactionRecord list to JSON string."""
    data = [r.model_dump(mode="json") for r in records]
    return json.dumps(data, ensure_ascii=False, indent=2)


def json_to_records(json_str: str) -> list[TransactionRecord]:
    """Deserialize JSON string to TransactionRecord list."""
    data = json.loads(json_str)
    return [TransactionRecord(**item) for item in data]


# --- Private Helpers ---


def _build_from_matched(
    match_result: MatchResult,
) -> list[TransactionRecord]:
    """Build records from matched pairs via extraction."""
    pair_map: dict[int, MatchedPair] = {}
    extractions: list[ExtractionResult] = []

    for i, pair in enumerate(match_result.matched_pairs):
        extraction = extract_from_matched_pair(pair)
        extractions.append(extraction)
        pair_map[id(extraction)] = pair

    groups = group_by_time_window(extractions)
    return _assemble_from_groups(groups, pair_map)


def _assemble_from_groups(
    groups: list[list[ExtractionResult]],
    pair_map: dict[int, MatchedPair],
) -> list[TransactionRecord]:
    """Assemble TransactionRecord from grouped extractions."""
    records: list[TransactionRecord] = []
    for group in groups:
        record = _assemble_single_record(group, pair_map)
        records.append(record)
    return records


def _assemble_single_record(
    group: list[ExtractionResult],
    pair_map: dict[int, MatchedPair],
) -> TransactionRecord:
    """Assemble one TransactionRecord from a group."""
    primary = group[0]
    pair = pair_map[id(primary)]
    quantity = _sum_quantity(group)

    confidence = _calculate_confidence(
        pair.image_result.confidence, primary.confidence
    )
    needs_review = _determine_needs_review(
        confidence, pair.needs_review
    )
    status = resolve_payment_status(
        primary.quoted_amount, quantity,
        pair.image_result.amount,
    )
    notes = _build_notes(quantity)

    return TransactionRecord(
        transaction_date=primary.timestamp.date(),
        customer_name=primary.customer_name,
        repair_item=primary.repair_item,
        quoted_amount=primary.quoted_amount,
        received_amount=pair.image_result.amount,
        payment_method=pair.image_result.payment_method,
        payment_status=status,
        source_images=[pair.image_result.filename],
        confidence=confidence,
        needs_review=needs_review,
        notes=notes,
    )


def _build_unmatched_records(
    match_result: MatchResult,
) -> list[TransactionRecord]:
    """Build review-flagged records from unmatched images."""
    records: list[TransactionRecord] = []
    for image_result in match_result.unmatched_images:
        record = _build_unmatched_single(image_result)
        records.append(record)
    return records


def _build_unmatched_single(
    image_result: ImageAnalysisResult,
) -> TransactionRecord:
    """Build a single record from an unmatched image."""
    tx_date = (
        image_result.image_date
        or image_result.transaction_date
    )
    return TransactionRecord(
        transaction_date=tx_date or __import__("datetime").date.today(),
        customer_name="Unknown",
        repair_item=None,
        quoted_amount=None,
        received_amount=image_result.amount,
        payment_method=image_result.payment_method,
        payment_status="unpaid" if image_result.amount is None else "paid",
        source_images=[image_result.filename],
        confidence=round(image_result.confidence / 2, 2),
        needs_review=True,
        notes="Unmatched image — no message context",
    )


def _sum_quantity(group: list[ExtractionResult]) -> int:
    """Sum quantity from all extractions in a group."""
    return sum(e.quantity for e in group)


def _calculate_confidence(
    image_confidence: float,
    extraction_confidence: float,
) -> float:
    """Calculate overall confidence as average."""
    return round(
        (image_confidence + extraction_confidence) / 2, 2
    )


def _determine_needs_review(
    confidence: float, pair_needs_review: bool
) -> bool:
    """Determine if record needs manual review."""
    return confidence < REVIEW_THRESHOLD or pair_needs_review


def _build_notes(quantity: int) -> str:
    """Build notes string based on quantity."""
    if quantity > 1:
        return f"數量: {quantity}"
    return ""
