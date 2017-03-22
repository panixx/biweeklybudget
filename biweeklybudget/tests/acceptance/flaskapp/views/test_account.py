"""
The latest version of this package is available at:
<http://github.com/jantman/biweeklybudget>

################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of biweeklybudget, also known as biweeklybudget.

    biweeklybudget is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    biweeklybudget is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with biweeklybudget.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/biweeklybudget> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import pytest
from biweeklybudget.tests.acceptance_helpers import AcceptanceHelper


@pytest.mark.acceptance
@pytest.mark.usefixtures("testdb", "testflask")
class TestAccount(AcceptanceHelper):

    @pytest.fixture(autouse=True)
    def get_page(self, base_url, selenium):
        self.baseurl = base_url
        selenium.get(base_url + '/accounts/1')

    def test_heading(self, selenium):
        heading = selenium.find_element_by_class_name('navbar-brand')
        assert heading.text == 'BankOne - Budget App'

    def test_nav_links(self, selenium):
        nav = selenium.find_element_by_xpath(
            "//div[contains(@class, 'sidebar-nav')]/ul"
        )
        navlinks = []
        for li in nav.find_elements_by_xpath("//li/a"):
            if li.text.strip() == '':
                continue
            navlinks.append(
                (self.relurl(li.get_attribute('href')), li.text)
            )
        assert navlinks == [
            ('/', 'Home'),
            ('/payperiods', 'Calendar'),
            ('/accounts', 'Accounts'),
            ('/ofx', 'OFX'),
            ('/transactions', 'Transactions'),
            ('/reconcile', 'Reconcile'),
            ('/budgets', 'Budgets'),
            ('/scheduled', 'Scheduled'),
        ]

    def test_stale_accounts(self, selenium):
        div = selenium.find_elements_by_xpath(
            "//div[@id='notifications-row']/div/div"
        )[0]
        assert div.text == '2 Accounts with stale data. View Accounts.'
        a = div.find_element_by_tag_name('a')
        assert self.relurl(a.get_attribute('href')) == '/accounts'
        assert a.text == 'View Accounts'

    def test_unreconciled_transactions(self, selenium):
        div = selenium.find_elements_by_xpath(
            "//div[@id='notifications-row']/div/div"
        )[1]
        assert div.text == 'XX Unreconciled Transactions. (EXAMPLE) Alert Link.'
        a = div.find_element_by_tag_name('a')
        assert self.relurl(a.get_attribute('href')) == '/reconcile'
        assert a.text == 'Alert Link'


@pytest.mark.acceptance
@pytest.mark.usefixtures("testdb", "testflask")
class TestAccountBankOne(AcceptanceHelper):

    @pytest.fixture(autouse=True)
    def get_page(self, base_url, selenium):
        self.baseurl = base_url
        selenium.get(base_url + '/accounts/1')

    def test_heading(self, selenium):
        heading = selenium.find_element_by_class_name('navbar-brand')
        assert heading.text == 'BankOne - Budget App'

    def test_panel_heading(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        heading = panel.find_element_by_class_name('panel-heading')
        assert heading.text.strip() == 'BankOne (1)'
        assert heading.find_element_by_tag_name(
            'i').get_attribute('class') == 'fa fa-bank fa-fw'

    def test_acct_table(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        table = panel.find_element_by_tag_name('table')
        texts = self.tbody2textlist(table)
        elems = self.tbody2elemlist(table)
        assert texts[0:4] == [
            ['Description', 'First Bank Account'],
            ['Type', 'Bank'],
            ['Ledger Balance', '$12,789.01'],
            ['Available Balance', '$12,563.18']
        ]
        assert texts[4][0] == 'Last OFX Data'
        assert '(14 hours ago)' in texts[4][1]
        assert elems[4][1].get_attribute('class') == 'data_age'
        assert texts[5:] == [
            ['Active?', 'True'],
            ['OFXGetter Config', '{"foo": "bar"}'],
            ['ofx_cat_memo_to_name', 'True'],
            [
                'Interest Charge regex',
                '^(interest charge|purchase finance charge)'
            ],
            ['Interest Paid regex', '^interest paid'],
            [
                'Payment regex',
                '^(online payment|internet payment|online pymt|payment)'
            ],
            ['Fee regex', '^(late fee|past due fee)']
        ]


@pytest.mark.acceptance
@pytest.mark.usefixtures("testdb", "testflask")
class TestAccountBankTwoStale(AcceptanceHelper):

    @pytest.fixture(autouse=True)
    def get_page(self, base_url, selenium):
        self.baseurl = base_url
        selenium.get(base_url + '/accounts/2')

    def test_heading(self, selenium):
        heading = selenium.find_element_by_class_name('navbar-brand')
        assert heading.text == 'BankTwoStale - Budget App'

    def test_panel_heading(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        heading = panel.find_element_by_class_name('panel-heading')
        assert heading.text.strip() == 'BankTwoStale (2)'
        assert heading.find_element_by_tag_name(
            'i').get_attribute('class') == 'fa fa-bank fa-fw'

    def test_acct_table(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        table = panel.find_element_by_tag_name('table')
        texts = self.tbody2textlist(table)
        elems = self.tbody2elemlist(table)
        assert texts[0:3] == [
            ['Description', 'Stale Bank Account'],
            ['Type', 'Bank'],
            ['Ledger Balance', '$100.23']
        ]
        assert texts[3][0] == 'Last OFX Data'
        assert '(18 days ago)' in texts[3][1]
        assert elems[3][1].get_attribute('class') == 'data_age text-danger'
        assert texts[4:] == [
            ['Active?', 'True'],
            ['OFXGetter Config', '{"foo": "baz"}'],
            ['ofx_cat_memo_to_name', 'False'],
            [
                'Interest Charge regex',
                '^(interest charge|purchase finance charge)'
            ],
            ['Interest Paid regex', '^interest paid'],
            [
                'Payment regex',
                '^(online payment|internet payment|online pymt|payment)'
            ],
            ['Fee regex', '^(late fee|past due fee)']
        ]


@pytest.mark.acceptance
@pytest.mark.usefixtures("testdb", "testflask")
class TestAccountCreditOne(AcceptanceHelper):

    @pytest.fixture(autouse=True)
    def get_page(self, base_url, selenium):
        self.baseurl = base_url
        selenium.get(base_url + '/accounts/3')

    def test_heading(self, selenium):
        heading = selenium.find_element_by_class_name('navbar-brand')
        assert heading.text == 'CreditOne - Budget App'

    def test_panel_heading(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        heading = panel.find_element_by_class_name('panel-heading')
        assert heading.text.strip() == 'CreditOne (3)'
        assert heading.find_element_by_tag_name(
            'i').get_attribute('class') == 'fa fa-credit-card fa-fw'

    def test_acct_table(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        table = panel.find_element_by_tag_name('table')
        texts = self.tbody2textlist(table)
        elems = self.tbody2elemlist(table)
        assert texts[0:4] == [
            ['Description', 'First Credit Card, limit 2000'],
            ['Type', 'Credit'],
            ['Ledger Balance', '$952.06'],
            ['Credit Limit', '$2,000.00']
        ]
        assert texts[4][0] == 'Last OFX Data'
        assert '(13 hours ago)' in texts[4][1]
        assert elems[4][1].get_attribute('class') == 'data_age'
        assert texts[5:] == [
            ['Active?', 'True'],
            ['OFXGetter Config', 'None'],
            ['ofx_cat_memo_to_name', 'False'],
            [
                'Interest Charge regex',
                '^(interest charge|purchase finance charge)'
            ],
            ['Interest Paid regex', '^interest paid'],
            [
                'Payment regex',
                '^(online payment|internet payment|online pymt|payment)'
            ],
            ['Fee regex', '^(late fee|past due fee)']
        ]


@pytest.mark.acceptance
@pytest.mark.usefixtures("testdb", "testflask")
class TestAccountCreditTwo(AcceptanceHelper):

    @pytest.fixture(autouse=True)
    def get_page(self, base_url, selenium):
        self.baseurl = base_url
        selenium.get(base_url + '/accounts/4')

    def test_heading(self, selenium):
        heading = selenium.find_element_by_class_name('navbar-brand')
        assert heading.text == 'CreditTwo - Budget App'

    def test_panel_heading(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        heading = panel.find_element_by_class_name('panel-heading')
        assert heading.text.strip() == 'CreditTwo (4)'
        assert heading.find_element_by_tag_name(
            'i').get_attribute('class') == 'fa fa-credit-card fa-fw'

    def test_acct_table(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        table = panel.find_element_by_tag_name('table')
        texts = self.tbody2textlist(table)
        elems = self.tbody2elemlist(table)
        assert texts[0:4] == [
            ['Description', 'Credit 2 limit 5500'],
            ['Type', 'Credit'],
            ['Ledger Balance', '$5,498.65'],
            ['Credit Limit', '$5,500.00']
        ]
        assert texts[4][0] == 'Last OFX Data'
        assert '(a day ago)' in texts[4][1]
        assert elems[4][1].get_attribute('class') == 'data_age'
        assert texts[5:] == [
            ['Active?', 'True'],
            ['OFXGetter Config', ''],
            ['ofx_cat_memo_to_name', 'False'],
            [
                'Interest Charge regex',
                '^(interest charge|purchase finance charge)'
            ],
            ['Interest Paid regex', '^interest paid'],
            [
                'Payment regex',
                '^(online payment|internet payment|online pymt|payment)'
            ],
            ['Fee regex', '^(late fee|past due fee)']
        ]


@pytest.mark.acceptance
@pytest.mark.usefixtures("testdb", "testflask")
class TestAccountInvestmentOne(AcceptanceHelper):

    @pytest.fixture(autouse=True)
    def get_page(self, base_url, selenium):
        self.baseurl = base_url
        selenium.get(base_url + '/accounts/5')

    def test_heading(self, selenium):
        heading = selenium.find_element_by_class_name('navbar-brand')
        assert heading.text == 'InvestmentOne - Budget App'

    def test_panel_heading(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        heading = panel.find_element_by_class_name('panel-heading')
        assert heading.text.strip() == 'InvestmentOne (5)'
        assert heading.find_element_by_tag_name(
            'i').get_attribute('class') == 'glyphicon glyphicon-piggy-bank'

    def test_acct_table(self, selenium):
        panel = selenium.find_element_by_id('panel-account')
        table = panel.find_element_by_tag_name('table')
        texts = self.tbody2textlist(table)
        elems = self.tbody2elemlist(table)
        assert texts[0:3] == [
            ['Description', 'Investment One Stale'],
            ['Type', 'Investment'],
            ['Ledger Balance', '$10,362.91']
        ]
        assert texts[3][0] == 'Last OFX Data'
        assert '(13 days ago)' in texts[3][1]
        assert elems[3][1].get_attribute('class') == 'data_age text-danger'
        assert texts[4:] == [
            ['Active?', 'True'],
            ['OFXGetter Config', ''],
            ['ofx_cat_memo_to_name', 'False'],
            [
                'Interest Charge regex',
                '^(interest charge|purchase finance charge)'
            ],
            ['Interest Paid regex', '^interest paid'],
            [
                'Payment regex',
                '^(online payment|internet payment|online pymt|payment)'
            ],
            ['Fee regex', '^(late fee|past due fee)']
        ]