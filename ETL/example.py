# -*- coding: utf-8 -*-
from lxml import etree


tree = etree.HTML("""
<div class="detailHeader VIEWDATA">
        <div class="title-wrapper" log-mod="detail_header">
            <div class="content">
                                    <span class="worth_position"></span>
                                <div class="title">
                    <h1 class="main" title="时代花生品质小区，精装修一房加储物间">
                        时代花生品质小区，精装修一房加储物间
                                                                                                </h1>
                    <div class="sub">
                                                    高楼层望白云山，视野无遮挡，采光很好，顶楼可以晾晒被子。
                                            </div>
                </div>
                                    <div class="btnContainer ">
                        <div>
                            <div class="action">
                                <button id="follow" class="followbtn" data-text="关注房源">
                                    关注房源</button>
                                <span id="favCount" class="count">42</span>人关注
                                <span class="layer-qrcode followLayer" style="display: none;">
                        <span class="icon-qrcode">
                          <img width="100" height="100" src="https://ajax.api.ke.com/qr/getDownloadQr?location=follow_app&amp;jweb_channel_key=ershoufang_view" alt="下载贝壳找房APP">
                        </span>
                        <span class="txt">下载贝壳找房APP</span>
                        <span class="sub-txt">房源动态早知道</span>
                        <span class="icon-close"></span>
                      </span>
                            </div>
                        </div>
                    </div>
                            </div>
        </div>
    </div>
    """)

elem = tree.xpath('//div[@class="sub"]/text()')
print(elem[0].strip())
# print(etree.tostring(elem, method='html', encoding='utf-8').decode('utf-8'))