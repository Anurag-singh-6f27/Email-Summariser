from mail.parser import (
    decode_header_value,
    extract_email_address,
    extract_sender_name,
    html_to_text,
)

print(decode_header_value("Hello"))
print(extract_email_address("GitHub <noreply@github.com>"))
print(extract_sender_name("GitHub <noreply@github.com>"))

html = """
<html>
    <body>
        <h1>Hello</h1>
        <p>This is a <b>test</b>.</p>
    </body>
</html>
"""

print(html_to_text(html))