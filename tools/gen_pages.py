import re, os, json
ROOT = os.path.join(os.path.dirname(__file__), '..', 'site-root')
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

# language page definitions: slug, name, dialects, note
PAGES = [
 ("spanish","Spanish",["Argentinian","Mexican","Colombian","Spain","Chilean","Peruvian","Venezuelan","Caribbean","US Latino"],
  "Spanish changes a lot from one country to the next. A Mexican audience hears a different voice than a Rioplatense one, and vos versus tú is only the start. Pick the market and the rewrite follows its vocabulary, its rhythm and its level of formality."),
 ("french","French",["France","Canadian (Quebec)","Belgian","Swiss","West African"],
  "French for Paris and French for Montreal are not interchangeable. Tone, vocabulary and the way you address a customer all shift. Choose the market and get copy that reads like it was written there."),
 ("portuguese","Portuguese",["Brazilian","European (Portugal)"],
  "Brazilian and European Portuguese differ in spelling, grammar and everyday words, and readers notice at once. Transcreate writes for the one you choose instead of blending them."),
 ("german","German",["Germany","Austrian","Swiss"],
  "German marketing copy lives or dies on register: du or Sie, direct or restrained. Pick the country and the rewrite keeps the meaning while sounding like a German speaker wrote it."),
 ("italian","Italian",[],
  "Italian rewards warmth and rhythm, and punishes literal English sentence structure. Transcreate rebuilds your line the way an Italian copywriter would."),
 ("chinese","Chinese",["Simplified (Mandarin)","Traditional (Taiwan)","Cantonese (Hong Kong)"],
  "Simplified Mandarin, Traditional Taiwanese Chinese and Hong Kong Cantonese are three different reading experiences. Choose one and get wording that fits it, not a character swap."),
 ("japanese","Japanese",[],
  "Japanese depends on politeness level and on what is left unsaid. A direct translation from English often sounds abrupt or oddly formal. Transcreate adjusts both."),
 ("korean","Korean",[],
  "Korean speech levels and word choice carry a lot of meaning. Transcreate writes in a register that suits the message instead of translating sentence by sentence."),
 ("arabic","Arabic",["Modern Standard","Egyptian","Gulf","Levantine","Moroccan"],
  "Modern Standard Arabic is right for formal writing, but spoken markets respond to their own dialects. Pick Egyptian, Gulf, Levantine or Moroccan and get copy that sounds local."),
 ("russian","Russian",[],
  "Russian copy built on English sentence patterns reads as translated almost immediately. Transcreate restructures the line so it sounds like it started in Russian."),
 ("hindi","Hindi",[],
  "Hindi readers mix registers and borrow English words freely. Transcreate finds the balance that sounds natural for your message instead of translating word for word."),
 ("english","English",["American","British","Australian","Canadian","Irish","Indian"],
  "Transcreation works into English too. Take text written in another language, or English from another market, and make it sound American, British, Australian, Canadian, Irish or Indian."),
 ("turkish","Turkish",[],
  "Turkish word order and politeness differ sharply from English. Transcreate rewrites your text so it reads as native Turkish, not as a translation."),
 ("dutch","Dutch",[],
  "Dutch is direct, informal and allergic to hype. Transcreate rebuilds your message to match that tone instead of carrying over English enthusiasm."),
]

def sub(s, pat, rep, count=1):
    out, n = re.subn(pat, lambda m: rep, s, count=count, flags=re.S)
    assert n >= 1, pat
    return out

for slug, name, dialects, note in PAGES:
    p = src
    url = f"https://transcreate.com/{slug}/"
    title = f"Transcreate into {name}: free, native-sounding {name} | Transcreate"
    desc = f"Free AI transcreation into {name}. Paste your text, pick a dialect, and get a rewrite that sounds written in {name}, not translated. No sign-up."
    p = sub(p, r'<title>.*?</title>', f'<title>{title}</title>')
    p = sub(p, r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">')
    p = sub(p, r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{url}">')
    p = sub(p, r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="{url}">')
    p = sub(p, r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="Transcreate into {name}. Say it like a native.">')
    p = sub(p, r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{desc}">')
    p = p.replace('"url":"https://transcreate.com/"', f'"url":"{url}"')
    p = p.replace('"name":"Transcreate","url"', f'"name":"Transcreate into {name}","url"')
    # about block
    dl = (f"<p>Dialects available: {', '.join(dialects)}.</p>" if dialects else "")
    about = (f'<section class="about"><div class="wrap">\n'
             f'<h2>Transcreate into {name}</h2>\n<p>{note}</p>\n{dl}\n'
             f'<p>Paste your text in any language, choose {name}{" and a dialect" if dialects else ""}, and copy the result. It is free and needs no account.</p>\n'
             f'<p><a href="/">See all 21 languages</a></p>\n</div></section>')
    p = sub(p, r'<section class="about">.*?</section>', about)
    p = sub(p, r'window\.PRESET\s*=\s*null;', f'window.PRESET = "{name}";')
    d = os.path.join(ROOT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(p)

# sitemap
urls = ["https://transcreate.com/"] + [f"https://transcreate.com/{s}/" for s,_,_,_ in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for i,u in enumerate(urls):
    sm += f'  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{"1.0" if i==0 else "0.7"}</priority></url>\n'
sm += '</urlset>\n'
open(os.path.join(ROOT,'sitemap.xml'),'w').write(sm)
print(len(PAGES),'pages')
