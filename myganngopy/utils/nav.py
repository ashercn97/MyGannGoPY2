from playwright.async_api import async_playwright, Page

class Action:
    def __init__(self, page: Page, action_type: str, log=False, test=False, browser=None):
        self.page = page
        self.action_type = action_type
        self.log = log
        self.test = test
        self.browser = browser

    async def run(self, item):
        if self.action_type == "hover":
            await self._hover(item)
        elif self.action_type == "click":
            await self._click(item)
        elif self.action_type == "hover_click":
            await self._hover_click(item)
        else:
            raise ValueError("Action type not supported.")

    async def _hover(self, selector):
        element = await self.page.wait_for_selector(selector)
        await element.hover()
        if self.log:
            print(f"Hovered over {selector}")
        await self.page.wait_for_timeout(5000)

    async def _click(self, selector):
        await self.page.click(selector)
        if self.log:
            print(f"Clicked {selector}")
        await self.page.wait_for_timeout(5000)

    async def _hover_click(self, selector):
        element = await self.page.wait_for_selector(selector)
        await element.hover()
        await self.page.wait_for_timeout(1000)  # wait before click
        await element.click()
        if self.log:
            print(f"Hovered and clicked on {selector}")

class NavItem:
    def __init__(self, name, xpath, action_type="click"):
        self.name = name
        self.xpath = xpath
        self.action_type = action_type

# everything is self explanitory, except callback
# callback is a function that takes the config as an arg, and does something
# my idea is it will probably do some navigation stuff...
class NavParent:
    def __init__(self, name, config, xpath=None, action_type=None, children=None, callback=None):
        self.name = name
        self.xpath = xpath
        self.action_type = action_type
        self.children = children if children else []
        self.config = config
        self.callback = callback

    async def run(self, child_name):
        await self.callback(self.config) if self.callback else None
        if self.xpath:
            parent_action = Action(self.config['page'], self.action_type, log=self.config['log'], test=self.config['test'], browser=self.config['browser'])
            await parent_action.run(self.xpath)

        child = next((c for c in self.children if c.name == child_name), None)
        if child:
            child_action = Action(self.config['page'], child.action_type, log=self.config['log'], test=self.config['test'], browser=self.config['browser'])
            await child_action.run(child.xpath)
        else:
            raise ValueError(f"Child {child_name} not found in {self.name}")

class NavNested:
    def __init__(self, config):
        self.config = config
        self.initialize_navigation()

    def initialize_navigation(self):
        self.progress_navbar = NavParent(
            name="Progress_Navbar",
            config=self.config,
            action_type="click",
            children=[
                NavItem(name="Progress_Button_List", xpath="xpath=/html/body/div[2]/div/div[6]/div[3]/div/ul/li[1]/a", action_type="click"),
                NavItem(name="Schedule_Button_List", xpath="xpath=/html/body/div[2]/div/div[6]/div[3]/div/ul/li[2]/a", action_type="click")
            ]
        )

        self.my_day_hover = NavParent(
            name="My_Day_Hover",
            config=self.config,
            xpath="xpath=/html/body/div[2]/div/div[6]/div[2]/div[1]/div/div/div/ul/li[1]/a/span[1]/span",
            action_type="hover",
            children=[
                NavItem(name="Progress_Button", xpath="xpath=/html/body/div[2]/div/div[6]/div[2]/div[1]/div/div/div/ul/li[1]/div[2]/ul/li[1]/a", action_type="click"),
                NavItem(name="Schedule_Button", xpath="xpath=/html/body/div[2]/div/div[6]/div[2]/div[1]/div/div/div/ul/li[1]/div[2]/ul/li[2]/a", action_type="click"),
                NavItem(name="Assignment_Center_Button", xpath="xpath=/html/body/div[2]/div/div[6]/div[2]/div[1]/div/div/div/ul/li[1]/div[2]/ul/li[3]/a", action_type="click"),
                NavItem(name="Conduct_Button", xpath="xpath=/html/body/div[2]/div/div[6]/div[2]/div[1]/div/div/div/ul/li[1]/div[2]/ul/li[4]/a", action_type="click")
            ]
        )

        async def assignment_center_callback(config):
            navigation = NavNested(config)
            await navigation.my_day_hover.run("Assignment_Center_Button")


        self.report_dropdown = NavParent(
            name="Report_Dropdown",
            config=self.config,
            action_type="click",
            callback=assignment_center_callback,
            xpath="xpath=/html/body/div[2]/div/div[14]/div[1]/div/div/section/div[2]/div/div[1]/div/div/div/div[1]/div/div[3]/div/button[2]",
            children=[
                NavItem(name="View_Assignment_Grades", xpath="xpath=/html/body/div[2]/div/div[14]/div[1]/div/div/section/div[2]/div/div[1]/div/div/div/div[1]/div/div[3]/div/ul/li[1]/a", action_type="click"),
            ]

        )

        self.profile_dropdown = NavParent(
            name="Profile_Dropdown",
            config=self.config,
            action_type="click",
            xpath="xpath=/html/body/div[2]/div/div[6]/div[1]/div[1]/div/div/div[4]/div/ul/li[4]/a",
            children=[
                NavItem(name="Profile_Dropdown_Profile", xpath="xpath=/html/body/div[2]/div/div[6]/div[1]/div[1]/div/div/div[4]/div/ul/li[4]/div[2]/ul/li[1]/a", action_type="click"),
            ]
        )