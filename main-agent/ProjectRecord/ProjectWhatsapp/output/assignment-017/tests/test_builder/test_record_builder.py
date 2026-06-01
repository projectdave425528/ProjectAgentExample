"""Tests for record_builder — main integration logic.

Covers:
- Happy Path: build_records with matched messages/images
- Error Path: empty inputs, all unmatched
- Edge Case: low confidence, unique IDs, JSON round-trip
- Integration: full pipeline from messages + images to records
"""
import json
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest

from src.builder.record_builder import (
    build_records,
    records_to_json,
    json_to_records,
    _calculate_confidence,
    _determine_needs_review,
    _build_notes,
    _sum_quantity,
    REVIEW_THRESHOLD,
)
from src.builder.matcher import MatchResult, MatchedPair
from src.builder.extractor import ExtractionResult
from src.models.message import ParsedMessage
from src.models.image_result import ImageAnalysisResult
from src.models.transaction import TransactionRecord


# --- Fixtures ---


def _make_message(
    sender="Chen",
    content="換屏 $500",
    timestamp=None,
    attachments=None,
):
    """Create a test ParsedMessage."""
    return ParsedMessage(
        timestamp=timestamp or datetime(2026, 5, 30, 10, 0),
        sender=sender,
        content=content,
        attachments=attachments or ["img001.jpg"],
        raw_text=f"[10:00] {sender}: {content}",
    )


def _make_image_result(
    filename="img001.jpg",
    amount=Decimal("500"),
    confidence=0.9,
    payment_method="payme",
    needs_review=False,
    error=None,
):
    """Create a test ImageAnalysisResult."""
    return ImageAnalysisResult(
        filename=filename,
        analysis_mode="ocr",
        amount=amount,
        confidence=confidence,
        payment_method=payment_method,
        needs_review=needs_review,
        error=error,
    )


# --- Unit Tests: Helper Functions ---


class TestCalculateConfidence:
    """Tests for _calculate_confidence."""

    def test_average_of_two_scores(self):
        result = _calculate_confidence(0.9, 0.7)
        assert result == 0.8

    def test_rounds_to_two_decimals(self):
        result = _calculate_confidence(0.85, 0.77)
        assert result == 0.81

    def test_both_zero(self):
        result = _calculate_confidence(0.0, 0.0)
        assert result == 0.0

    def test_both_one(self):
        result = _calculate_confidence(1.0, 1.0)
        assert result == 1.0


class TestDetermineNeedsReview:
    """Tests for _determine_needs_review."""

    def test_low_confidence_triggers_review(self):
        assert _determine_needs_review(0.5, False) is True

    def test_pair_needs_review_triggers_review(self):
        assert _determine_needs_review(0.8, True) is True

    def test_high_confidence_no_pair_flag(self):
        assert _determine_needs_review(0.8, False) is False

    def test_exactly_at_threshold(self):
        # confidence < 0.6 triggers, so 0.6 should NOT trigger
        assert _determine_needs_review(0.6, False) is False

    def test_just_below_threshold(self):
        assert _determine_needs_review(0.59, False) is True


class TestBuildNotes:
    """Tests for _build_notes."""

    def test_quantity_one_returns_empty(self):
        assert _build_notes(1) == ""

    def test_quantity_greater_than_one(self):
        assert _build_notes(3) == "數量: 3"

    def test_quantity_two(self):
        assert _build_notes(2) == "數量: 2"


class TestSumQuantity:
    """Tests for _sum_quantity."""

    def test_single_item(self):
        results = [
            ExtractionResult(
                customer_name="A",
                timestamp=datetime(2026, 1, 1),
                quantity=2,
            )
        ]
        assert _sum_quantity(results) == 2

    def test_multiple_items(self):
        results = [
            ExtractionResult(
                customer_name="A",
                timestamp=datetime(2026, 1, 1),
                quantity=2,
            ),
            ExtractionResult(
                customer_name="A",
                timestamp=datetime(2026, 1, 1),
                quantity=3,
            ),
        ]
        assert _sum_quantity(results) == 5


# --- Unit Tests: records_to_json / json_to_records ---


class TestJsonSerialization:
    """Tests for JSON serialization round-trip."""

    def test_round_trip_single_record(self):
        record = TransactionRecord(
            transaction_date=date(2026, 5, 30),
            customer_name="Chen",
            repair_item="換屏",
            quoted_amount=Decimal("500"),
            received_amount=Decimal("500"),
            payment_method="payme",
            payment_status="paid",
            source_images=["img001.jpg"],
            confidence=0.85,
            needs_review=False,
            notes="",
        )
        json_str = records_to_json([record])
        restored = json_to_records(json_str)

        assert len(restored) == 1
        assert restored[0].customer_name == "Chen"
        assert restored[0].repair_item == "換屏"
        assert restored[0].payment_status == "paid"
        assert restored[0].confidence == 0.85

    def test_round_trip_multiple_records(self):
        records = [
            TransactionRecord(
                transaction_date=date(2026, 5, 30),
                customer_name=f"Customer{i}",
                payment_status="paid",
                confidence=0.8,
            )
            for i in range(3)
        ]
        json_str = records_to_json(records)
        restored = json_to_records(json_str)
        assert len(restored) == 3

    def test_round_trip_preserves_id(self):
        record = TransactionRecord(
            transaction_date=date(2026, 5, 30),
            customer_name="Test",
            payment_status="paid",
            confidence=0.8,
        )
        original_id = record.id
        json_str = records_to_json([record])
        restored = json_to_records(json_str)
        assert restored[0].id == original_id

    def test_empty_list_round_trip(self):
        json_str = records_to_json([])
        restored = json_to_records(json_str)
        assert restored == []

    def test_json_output_is_valid_json(self):
        record = TransactionRecord(
            transaction_date=date(2026, 5, 30),
            customer_name="Test",
            payment_status="unpaid",
            confidence=0.5,
        )
        json_str = records_to_json([record])
        parsed = json.loads(json_str)
        assert isinstance(parsed, list)
        assert len(parsed) == 1


# --- Integration Tests: build_records ---


class TestBuildRecordsHappyPath:
    """Happy path tests for build_records."""

    def test_single_message_single_image(self):
        messages = [_make_message()]
        images = [_make_image_result()]

        records = build_records(messages, images)

        assert len(records) == 1
        r = records[0]
        assert r.customer_name == "Chen"
        assert r.repair_item == "換屏"
        assert r.quoted_amount == Decimal("500")
        assert r.received_amount == Decimal("500")
        assert r.payment_method == "payme"
        assert r.payment_status == "paid"
        assert r.source_images == ["img001.jpg"]
        assert r.transaction_date == date(2026, 5, 30)

    def test_multiple_messages_multiple_images(self):
        messages = [
            _make_message(
                sender="CustomerA",
                content="換電池 $300",
                attachments=["a.jpg"],
                timestamp=datetime(2026, 5, 30, 9, 0),
            ),
            _make_message(
                sender="CustomerB",
                content="換屏 $500",
                attachments=["b.jpg"],
                timestamp=datetime(2026, 5, 30, 10, 0),
            ),
            _make_message(
                sender="CustomerC",
                content="維修 $800",
                attachments=["c.jpg"],
                timestamp=datetime(2026, 5, 30, 11, 0),
            ),
        ]
        images = [
            _make_image_result("a.jpg", Decimal("300")),
            _make_image_result("b.jpg", Decimal("500")),
            _make_image_result("c.jpg", Decimal("800")),
        ]

        records = build_records(messages, images)

        assert len(records) == 3
        names = {r.customer_name for r in records}
        assert names == {"CustomerA", "CustomerB", "CustomerC"}

    def test_five_messages_three_images(self):
        """5 messages + 3 images produces 3 matched records."""
        messages = [
            _make_message(
                sender=f"Customer{i}",
                content=f"換屏 ${i * 100 + 100}",
                attachments=[f"img{i}.jpg"] if i < 3 else [],
                timestamp=datetime(2026, 5, 30, 9 + i, 0),
            )
            for i in range(5)
        ]
        images = [
            _make_image_result(
                f"img{i}.jpg", Decimal(str(i * 100 + 100))
            )
            for i in range(3)
        ]

        records = build_records(messages, images)

        # Should produce records for the 3 matched pairs
        assert len(records) == 3

    def test_confidence_calculation(self):
        messages = [_make_message()]
        images = [_make_image_result(confidence=0.9)]

        records = build_records(messages, images)

        # extraction confidence for "換屏 $500" = 0.3 + 0.35 + 0.35 = 1.0
        # overall = (0.9 + 1.0) / 2 = 0.95
        assert records[0].confidence == 0.95

    def test_quantity_in_notes(self):
        messages = [
            _make_message(content="換屏 x3 $500")
        ]
        images = [_make_image_result()]

        records = build_records(messages, images)

        assert records[0].notes == "數量: 3"

    def test_payment_status_partial(self):
        messages = [
            _make_message(content="換屏 x2 $500")
        ]
        # quoted=500, qty=2, total=1000, received=700 -> partial
        images = [_make_image_result(amount=Decimal("700"))]

        records = build_records(messages, images)

        assert records[0].payment_status == "partial"


class TestBuildRecordsErrorPath:
    """Error path tests for build_records."""

    def test_empty_messages_and_images(self):
        records = build_records([], [])
        assert records == []

    def test_empty_messages_with_images(self):
        images = [_make_image_result()]
        records = build_records([], images)
        # All images unmatched -> produces unmatched records
        assert len(records) == 1
        assert records[0].needs_review is True

    def test_messages_without_matching_images(self):
        messages = [_make_message(attachments=["x.jpg"])]
        images = [_make_image_result("y.jpg")]
        # No match -> unmatched image record
        records = build_records(messages, images)
        assert len(records) == 1
        assert records[0].needs_review is True
        assert records[0].customer_name == "Unknown"

    def test_all_unmatched_still_produces_records(self):
        """Matcher returns all unmatched -> still get records."""
        images = [
            _make_image_result(f"unmatched{i}.jpg")
            for i in range(3)
        ]
        records = build_records([], images)
        assert len(records) == 3
        for r in records:
            assert r.needs_review is True


class TestBuildRecordsEdgeCases:
    """Edge case tests for build_records."""

    def test_all_records_unique_ids(self):
        messages = [
            _make_message(
                sender=f"Customer{i}",
                content=f"換屏 ${i * 100 + 100}",
                attachments=[f"img{i}.jpg"],
                timestamp=datetime(2026, 5, 30, 9 + i, 0),
            )
            for i in range(5)
        ]
        images = [
            _make_image_result(
                f"img{i}.jpg", Decimal(str(i * 100 + 100))
            )
            for i in range(5)
        ]

        records = build_records(messages, images)

        ids = [r.id for r in records]
        assert len(ids) == len(set(ids))

    def test_all_low_confidence_flagged_review(self):
        """All records with confidence < threshold -> needs_review."""
        messages = [_make_message(content="hello")]
        images = [
            _make_image_result(confidence=0.3)
        ]

        records = build_records(messages, images)

        # extraction confidence for no repair + no amount = 0.3
        # overall = (0.3 + 0.3) / 2 = 0.3 < 0.6
        for r in records:
            assert r.needs_review is True

    def test_needs_review_from_pair_flag(self):
        """MatchedPair.needs_review propagates to record."""
        messages = [_make_message()]
        images = [
            _make_image_result(
                error="OCR failed", needs_review=True
            )
        ]

        records = build_records(messages, images)

        assert records[0].needs_review is True

    def test_json_round_trip_after_build(self):
        """Records from build_records survive JSON round-trip."""
        messages = [_make_message()]
        images = [_make_image_result()]

        records = build_records(messages, images)
        json_str = records_to_json(records)
        restored = json_to_records(json_str)

        assert len(restored) == len(records)
        assert restored[0].customer_name == records[0].customer_name
        assert restored[0].payment_status == records[0].payment_status
        assert restored[0].id == records[0].id

    def test_no_quoted_amount_with_received(self):
        """No quoted amount but has received -> paid."""
        messages = [_make_message(content="幫我整下")]
        images = [_make_image_result(amount=Decimal("300"))]

        records = build_records(messages, images)

        assert records[0].payment_status == "paid"
        assert records[0].quoted_amount is None
