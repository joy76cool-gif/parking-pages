import pathlib
from playwright.sync_api import sync_playwright
f=pathlib.Path('晨間簡報_測.html').resolve()
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w,h,sch,touch in [('1920',1920,950,'light',False),('1366',1366,768,'light',False),('375',375,800,'light',True),('320',320,700,'light',True),('1920d',1920,950,'dark',False)]:
        ctx=b.new_context(viewport={'width':w,'height':h},color_scheme=sch,has_touch=touch,is_mobile=touch);pg=ctx.new_page();e=[]
        pg.on('pageerror',lambda x:e.append(str(x)));pg.goto(f.as_uri());pg.wait_for_timeout(1200)
        st=pg.evaluate("({ttl:document.querySelector('#mapttl').textContent,sel:document.querySelectorAll('details.sel').length,lead:getComputedStyle(document.querySelector('.lead')).fontSize,num:getComputedStyle(document.querySelector('.steps b')).fontSize,lab:getComputedStyle(document.querySelector('.steps span')).fontSize,sw:document.documentElement.scrollWidth,title:document.querySelectorAll('.nm[title]').length})")
        print(name,'start',st,e[:1]); pg.screenshot(path=f'v_{name}_0.png')
        pg.click('details[data-i=\"0\"] summary'); pg.wait_for_timeout(900)
        st=pg.evaluate("({ttl:document.querySelector('#mapttl').textContent,lbl:document.querySelectorAll('#lots text').length,g:!!document.querySelector('a.gmap'),sw:document.documentElement.scrollWidth})")
        print(name,'pick',st,e[:1])
        if w<1000: pg.evaluate("document.querySelector('#mapbox').scrollIntoView()"); pg.wait_for_timeout(300)
        pg.screenshot(path=f'v_{name}_1.png'); ctx.close()
    b.close()
