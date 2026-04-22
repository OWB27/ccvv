from app.services.resume_text_cleaner import build_text_preview, clean_resume_text


def test_clean_resume_text_normalizes_spaces_and_blank_lines():
    raw_text = " 张三 \r\n\r\n\r\n Python\t后端工程师 \x00\n\n\n 熟悉 FastAPI "

    cleaned = clean_resume_text(raw_text)

    assert "\x00" not in cleaned
    assert "\r" not in cleaned
    assert "Python 后端工程师" in cleaned
    assert "\n\n\n" not in cleaned
    assert cleaned.startswith("张三")


def test_build_text_preview_truncates_long_text():
    preview = build_text_preview("a" * 20, max_length=8)

    assert preview == "aaaaaaaa..."

