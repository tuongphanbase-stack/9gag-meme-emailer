# PARTIAL RECOVERY -- 9gag-meme-emailer
#
# This is the ONLY function from 9gag_top_meme_emailer.py that I have a
# verified, correctly-formatted copy of -- the foldable-cards version
# written earlier in our chat. It is not runnable on its own.
#
# I do NOT have working/reliable code for the rest of the project:
#   - fetching 9gag's hot feed, downloading/classifying/compressing images
#   - load_sent_ids / save_sent_ids
#   - build_html, build_plain_text
#   - the SMTP send step, cmd_generate / cmd_send (CLI entry points)
#   - .github/workflows/send-meme.yml
# The one earlier fetch that had all of that was a real read of your repo,
# but it came back with every line's indentation stripped (a side effect of
# how the page was extracted), and that raw result is no longer in my
# context -- only my notes and descriptions of it survived, not the source
# itself. Re-typing Python from a description risks silently wrong code, so
# I'm not presenting anything beyond this one function as "recovered."
#
# This function expects, at module level:
#   from html import escape
#   from urllib.parse import quote

def build_section_html(title, emoji, memes, columns, image_base_url):
    if not memes:
        return f"""
<h2 style="color:#222; font-family:Arial,Helvetica,sans-serif;">{emoji} New {title}</h2>
<p style="color:#999; font-size:13px; font-family:Arial,Helvetica,sans-serif;">No new qualifying posts since the last check.</p>"""

    cards = []
    for m in memes:
        raw_title = m["title"]
        title_esc = escape(raw_title)
        # Short teaser for the summary bar; full title still shows once expanded.
        teaser_raw = raw_title if len(raw_title) <= 70 else raw_title[:68].rsplit(" ", 1)[0] + "…"
        teaser_esc = escape(teaser_raw)
        img_url = f"{image_base_url}/{quote(m['filename'])}"
        play_badge = (
            '<span style="position:absolute; top:6px; right:6px; background:rgba(0,0,0,0.65); '
            'color:#fff; font-size:12px; padding:2px 7px; border-radius:12px;">&#9654; GIF</span>'
            if m["has_gif_preview"] else ""
        )
        note = (
            '<div style="font-size:11px; color:#4a90d9; margin-top:4px;">Animated preview</div>'
            if m["has_gif_preview"] else ""
        )
        cards.append(f"""
<td style="padding:8px; vertical-align:top; width:{100 // columns}%;">
<details open style="border:1px solid #e0e0e0; border-radius:10px; overflow:hidden; font-family:Arial,Helvetica,sans-serif;">
<summary style="cursor:pointer; padding:10px; background:#fafafa; border-bottom:1px solid #e0e0e0; font-size:13px; color:#222;">
<span style="color:#888;">#{m['rank']}</span>&nbsp;{teaser_esc}&nbsp;<span style="color:#888; white-space:nowrap;">&#9650; {m['votes']:,}</span>
</summary>
<a href="{escape(m['post_url'])}" style="text-decoration:none; color:inherit;">
<div style="position:relative;">
<img src="{escape(img_url)}" alt="{title_esc}" style="display:block; width:100%; height:auto; max-height:500px; object-fit:contain; background:#f5f5f5;">
{play_badge}
</div>
<div style="padding:10px;">
<div style="font-size:13px; color:#222; line-height:1.35;">{title_esc}</div>
<div style="font-size:12px; color:#888; margin-top:6px;">&#9650; {m['votes']:,} upvotes</div>
{note}
</div>
</a>
</details>
</td>""")

    rows = []
    for i in range(0, len(cards), columns):
        row_cards = cards[i:i + columns]
        row_cards += ["<td></td>"] * (columns - len(row_cards))
        rows.append(f"<tr>{''.join(row_cards)}</tr>")

    return f"""
<h2 style="color:#222; font-family:Arial,Helvetica,sans-serif;">{emoji} {len(memes)} New {title}</h2>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:900px;">
{''.join(rows)}
</table>"""
