"""Unit tests for src.builder.matcher module.

Covers:
- Happy Path: correct matching of images to messages
- Error Path: empty inputs, no matches
- Edge Cases: case-insensitive, duplicate filenames, error images
"""
import logging
from datetime import datetime, date
from decimal import Decimal

import pytest

from src.models.message import ParsedMessage
from src.models.image_result import ImageAnalysisResult
from src.builder.matcher import (
    MatchedPair,
    MatchResult,
    match_images_to_messages,
)


# --- Fixtures ---


def _make_message(
    sender: str,
    content: str,
    attachments: list[str] | None = None,
) -> ParsedMessage:
    """Helper to create a ParsedMessage for testing."""
    return ParsedMessage(
        timestamp=datetime(2024, 1, 15, 14, 30, 0),
        sender=sender,
        content=content,
        attachments=attachments or [],
        raw_text=f"[2024/01/15, 14:30:00] {sender}: {content}",
    )


def _make_image_result(
    filename: str,
    amount: Decimal | None = None,
    error: str | None = None,
    needs_review: bool = False,
) -> ImageAnalysisResult:
    """Helper to create an ImageAnalysisResult for testing."""
    return ImageAnalysisResult(
        filename=filename,
        analysis_mode="ocr",
        payment_method="payme",
        amount=amount,
        confidence=0.85,
        error=error,
        needs_review=needs_review,
    )


# --- Happy Path Tests ---


class TestMatchImagesHappyPath:
    """Happy path: correct matching scenarios."""

    def test_three_messages_three_images_all_match(self):
        """3 messages with attachments + 3 matching images = 3 pairs."""
        messages = [
            _make_message("Alice", "付款截圖", ["img001.jpg"]),
            _make_message("Bob", "收據", ["img002.png"]),
            _make_message("Charlie", "轉帳", ["img003.webp"]),
        ]
        image_results = [
            _make_image_result("img001.jpg", Decimal("500.00")),
            _make_image_result("img002.png", Decimal("300.00")),
            _make_image_result("img003.webp", Decimal("1000.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 3
        assert len(result.unmatched_images) == 0
        assert len(result.unmatched_attachments) == 0

    def test_matched_pair_contains_correct_message(self):
        """MatchedPair should reference the correct message."""
        messages = [
            _make_message("Alice", "PayMe 截圖", ["receipt.jpg"]),
        ]
        image_results = [
            _make_image_result("receipt.jpg", Decimal("200.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        pair = result.matched_pairs[0]
        assert pair.message.sender == "Alice"
        assert pair.message.content == "PayMe 截圖"
        assert pair.image_result.amount == Decimal("200.00")
        assert pair.needs_review is False

    def test_partial_match_some_unmatched(self):
        """Some images match, some don't."""
        messages = [
            _make_message("Alice", "截圖", ["img001.jpg"]),
        ]
        image_results = [
            _make_image_result("img001.jpg", Decimal("500.00")),
            _make_image_result("img999.jpg", Decimal("100.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 1
        assert len(result.unmatched_images) == 1
        assert result.unmatched_images[0].filename == "img999.jpg"

    def test_message_without_attachment_ignored(self):
        """Messages without attachments don't affect matching."""
        messages = [
            _make_message("Alice", "Hello"),
            _make_message("Bob", "截圖", ["img001.jpg"]),
            _make_message("Charlie", "OK"),
        ]
        image_results = [
            _make_image_result("img001.jpg", Decimal("500.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 1
        assert result.matched_pairs[0].message.sender == "Bob"


# --- Error Path Tests ---


class TestMatchImagesErrorPath:
    """Error path: empty inputs and no-match scenarios."""

    def test_empty_image_results(self):
        """Empty image_results → empty matched, all attachments unmatched."""
        messages = [
            _make_message("Alice", "截圖", ["img001.jpg"]),
            _make_message("Bob", "收據", ["img002.png"]),
        ]

        result = match_images_to_messages(messages, [])

        assert len(result.matched_pairs) == 0
        assert len(result.unmatched_images) == 0
        assert len(result.unmatched_attachments) == 2
        assert "img001.jpg" in result.unmatched_attachments
        assert "img002.png" in result.unmatched_attachments

    def test_empty_messages(self):
        """Empty messages → empty result, no crash."""
        image_results = [
            _make_image_result("img001.jpg", Decimal("500.00")),
        ]

        result = match_images_to_messages([], image_results)

        assert len(result.matched_pairs) == 0
        assert len(result.unmatched_images) == 1
        assert len(result.unmatched_attachments) == 0

    def test_both_empty(self):
        """Both inputs empty → empty result, no crash."""
        result = match_images_to_messages([], [])

        assert len(result.matched_pairs) == 0
        assert len(result.unmatched_images) == 0
        assert len(result.unmatched_attachments) == 0

    def test_no_matching_filenames(self):
        """No filenames match → all unmatched."""
        messages = [
            _make_message("Alice", "截圖", ["photo_a.jpg"]),
        ]
        image_results = [
            _make_image_result("photo_b.jpg", Decimal("100.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 0
        assert len(result.unmatched_images) == 1
        assert len(result.unmatched_attachments) == 1

    def test_warning_logged_for_unmatched_image(self, caplog):
        """Warning should be logged when image has no matching message."""
        messages = [_make_message("Alice", "Hi")]
        image_results = [
            _make_image_result("orphan.jpg", Decimal("50.00")),
        ]

        with caplog.at_level(logging.WARNING):
            match_images_to_messages(messages, image_results)

        assert "orphan.jpg" in caplog.text


# --- Edge Case Tests ---


class TestMatchImagesEdgeCases:
    """Edge cases: case sensitivity, duplicates, error images."""

    def test_case_insensitive_matching(self):
        """Filename matching should be case-insensitive."""
        messages = [
            _make_message("Alice", "截圖", ["IMG001.JPG"]),
        ]
        image_results = [
            _make_image_result("img001.jpg", Decimal("500.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 1
        assert result.matched_pairs[0].message.sender == "Alice"

    def test_case_insensitive_reverse(self):
        """Image filename uppercase, message lowercase."""
        messages = [
            _make_message("Bob", "收據", ["receipt.png"]),
        ]
        image_results = [
            _make_image_result("RECEIPT.PNG", Decimal("300.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 1

    def test_duplicate_filename_only_first_message_matched(self):
        """Same filename in multiple messages → only first one matched."""
        messages = [
            _make_message("Alice", "第一次", ["shared.jpg"]),
            _make_message("Bob", "第二次", ["shared.jpg"]),
        ]
        image_results = [
            _make_image_result("shared.jpg", Decimal("500.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 1
        assert result.matched_pairs[0].message.sender == "Alice"

    def test_image_with_error_still_matched_needs_review(self):
        """Image with error field set → matched but needs_review=True."""
        messages = [
            _make_message("Alice", "截圖", ["broken.jpg"]),
        ]
        image_results = [
            _make_image_result(
                "broken.jpg",
                amount=None,
                error="OCR failed: image corrupted",
            ),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 1
        pair = result.matched_pairs[0]
        assert pair.needs_review is True
        assert pair.image_result.error == "OCR failed: image corrupted"

    def test_image_with_needs_review_flag(self):
        """Image with needs_review=True → pair also needs_review."""
        messages = [
            _make_message("Alice", "截圖", ["low_conf.jpg"]),
        ]
        image_results = [
            _make_image_result(
                "low_conf.jpg",
                amount=Decimal("100.00"),
                needs_review=True,
            ),
        ]

        result = match_images_to_messages(messages, image_results)

        assert result.matched_pairs[0].needs_review is True

    def test_multiple_attachments_in_one_message(self):
        """Message with multiple attachments can match multiple images."""
        messages = [
            _make_message(
                "Alice", "兩張截圖", ["img_a.jpg", "img_b.jpg"]
            ),
        ]
        image_results = [
            _make_image_result("img_a.jpg", Decimal("100.00")),
            _make_image_result("img_b.jpg", Decimal("200.00")),
        ]

        result = match_images_to_messages(messages, image_results)

        assert len(result.matched_pairs) == 2
        assert len(result.unmatched_attachments) == 0

    def test_unmatched_attachments_preserve_original_case(self):
        """Unmatched attachment filenames keep their original case."""
        messages = [
            _make_message("Alice", "截圖", ["MyFile.JPG"]),
        ]

        result = match_images_to_messages(messages, [])

        assert "MyFile.JPG" in result.unmatched_attachments

    def test_match_result_is_pydantic_model(self):
        """MatchResult should be serializable as Pydantic model."""
        result = match_images_to_messages([], [])

        data = result.model_dump()
        assert "matched_pairs" in data
        assert "unmatched_images" in data
        assert "unmatched_attachments" in data
