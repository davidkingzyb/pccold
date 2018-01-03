// 2018/1/2 by DKZ
const arguments = process.argv
const room_id = process.argv[3]
const puppeteer = require('puppeteer');
(async() => {
    const browser = await puppeteer.launch({
        args: [
            '--no-sandbox',
            '--ppapi-flash-version=28.0.0.126',
            '--ppapi-flash-path=/usr/lib/PepperFlash/libpepflashplayer.so',
        ],
        headless: false,
    });
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', request => {
        if (request.url.indexOf('lapi/live/getPlay') >= 0) {
            console.log(request);
            request.abort();
            console.log('### ok')
            process.exit();
        } else {
            console.log('@@@ ' + request.url)
            request.continue();
        }
    });
    try {
        await page.goto('http://www.douyu.com/' + room_id);
    } catch (e) {
        console.log('*** error', e)
        process.exit();
    }
    await page.screenshot({path: 'screenshot.png'});
    await browser.close();
    console.log('### puppeteer close')
})();
