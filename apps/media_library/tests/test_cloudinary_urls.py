"""Tests for Cloudinary URL helpers."""

from apps.media_library.cloudinary_urls import apply_cloudinary_transform, cloudinary_srcset


def test_apply_transform_inserts_after_upload() -> None:
    url = "https://res.cloudinary.com/demo/image/upload/v1/sample.jpg"
    out = apply_cloudinary_transform(url, "w_400,c_limit,q_auto,f_auto")
    assert out == "https://res.cloudinary.com/demo/image/upload/w_400,c_limit,q_auto,f_auto/v1/sample.jpg"


def test_apply_transform_passthrough_non_cloudinary() -> None:
    url = "https://example.com/photo.jpg"
    assert apply_cloudinary_transform(url, "w_400") == url


def test_cloudinary_srcset() -> None:
    url = "https://res.cloudinary.com/demo/image/upload/v1/sample.jpg"
    srcset = cloudinary_srcset(url, (400, 800), "w_{w},c_limit,q_auto,f_auto")
    assert "400w" in srcset
    assert "800w" in srcset
    assert srcset.count("upload/") == 2
