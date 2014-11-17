module.exports = {
  "Redo a free text search through Search History" : function (browser) {
    browser
      .url(browser.launchUrl)
      .waitForElementVisible('body', 1000, 'Page loads')
      .pause(1000)
      .setValue('input[name=identification]', 'admin')
      .setValue('input[name=password]', 'emif')
      .click('button[type=submit]')
      .waitForElementVisible('div[id=playground]', 3000, 'Login successful')
      .waitForElementVisible('#actions a[href="advsearch/history"]', 3000, 'Dashboards opens and link is visible')
      .click('#actions a[href="advsearch/history"]')
      .waitForElementVisible('#simple', 2000, 'Free Search history loads with success')
      .waitForElementVisible('.btn-info', 2000, 'Free Search History entries exist')
      .click('.btn-info:nth-child(1)')
      .assert.elementPresent('#results_size', 'Result loaded for simple search')
      .end();
  }
};
