import pathlib
d = pathlib.Path(__file__).parent
base = (d / "_base.svg.tmpl").read_text()
read_next = '''
  <!-- open book -->
  <g stroke="#B98E44" stroke-width="6" stroke-linejoin="round">
    <path d="M512 430 C450 392 360 384 300 400 V640 C360 624 450 632 512 670 Z" fill="#F1E0B8"/>
    <path d="M512 430 C574 392 664 384 724 400 V640 C664 624 574 632 512 670 Z" fill="#E8D2A2"/>
  </g>
  <g fill="none" stroke="#8C5C33" stroke-width="5" stroke-linecap="round" opacity="0.75">
    <path d="M336 452 C384 442 432 446 478 464"/><path d="M336 494 C384 484 432 488 478 506"/>
    <path d="M336 536 C384 526 432 530 478 548"/><path d="M336 578 C384 568 432 572 478 590"/>
    <path d="M546 464 C592 446 640 442 688 452"/><path d="M546 506 C592 488 640 484 688 494"/>
    <path d="M546 548 C592 530 640 526 688 536"/>
  </g>
  <path d="M512 430 V670" stroke="#8C5C33" stroke-width="6"/>
  <!-- ribbon bookmark -->
  <path d="M600 418 V560 L620 540 L640 560 V408" fill="#A3332A" stroke="#6E1E18" stroke-width="3"/>
  <text x="512" y="372" text-anchor="middle" font-family="Didot, 'Bodoni 72', serif" font-size="96" fill="url(#gold)">&#x2766;</text>
  <text x="512" y="752" text-anchor="middle" font-family="Didot, 'Bodoni 72', serif" font-style="italic" font-size="62" letter-spacing="4" fill="url(#gold)">read next</text>
'''
(d / "read-next.svg").write_text(base.replace("__GLYPH__", read_next))
