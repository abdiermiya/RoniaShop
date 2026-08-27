from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
import json
import os

APP_NAME = "رونیا شاپ"
DATA_FILE = "roniya_shop_data.json"
ADMIN_PASSWORD = "1234"

DEFAULT_PRODUCTS = {
    "شیر": 30000,
    "نان": 15000,
    "پنیر": 50000,
    "آب": 10000,
    "چیپس": 25000
}


class RoniyaShop(App):
    def build(self):
        self.title = APP_NAME
        self.products = self.load_products()
        self.cart = {}
        return self.shop_screen()

    def load_products(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("products", DEFAULT_PRODUCTS.copy())
            except Exception:
                pass
        return DEFAULT_PRODUCTS.copy()

    def save_products(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"products": self.products}, f, ensure_ascii=False, indent=2)

    def shop_screen(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=8)

        title = Label(
            text="رونیا شاپ",
            font_size="28sp",
            size_hint_y=None,
            height=55
        )
        root.add_widget(title)

        scroll = ScrollView()
        self.product_box = GridLayout(
            cols=1,
            spacing=8,
            padding=5,
            size_hint_y=None
        )
        self.product_box.bind(minimum_height=self.product_box.setter("height"))
        scroll.add_widget(self.product_box)
        root.add_widget(scroll)

        buttons = BoxLayout(size_hint_y=None, height=55, spacing=8)

        cart_btn = Button(text="🛒 سبد خرید")
        cart_btn.bind(on_press=self.show_cart)
        buttons.add_widget(cart_btn)

        admin_btn = Button(text="🔐 مدیریت")
        admin_btn.bind(on_press=self.admin_login)
        buttons.add_widget(admin_btn)

        root.add_widget(buttons)
        self.refresh_products()
        return root

    def refresh_products(self):
        self.product_box.clear_widgets()

        for name, price in self.products.items():
            row = BoxLayout(
                size_hint_y=None,
                height=65,
                spacing=6
            )

            info = Label(
                text=f"{name}\\n{price:,} تومان",
                font_size="17sp"
            )
            row.add_widget(info)

            btn = Button(
                text="افزودن",
                size_hint_x=None,
                width=100
            )
            btn.bind(on_press=lambda instance, n=name: self.add_to_cart(n))
            row.add_widget(btn)

            self.product_box.add_widget(row)

    def add_to_cart(self, name):
        self.cart[name] = self.cart.get(name, 0) + 1
        self.show_message("سبد خرید", f"{name} به سبد خرید اضافه شد.")

    def show_cart(self, instance=None):
        content = BoxLayout(orientation="vertical", padding=10, spacing=8)

        scroll = ScrollView()
        box = GridLayout(cols=1, spacing=6, size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        total = 0

        if not self.cart:
            box.add_widget(Label(
                text="سبد خرید خالی است.",
                size_hint_y=None,
                height=50
            ))
        else:
            for name, count in self.cart.items():
                price = self.products.get(name, 0)
                subtotal = price * count
                total += subtotal

                box.add_widget(Label(
                    text=f"{name} × {count} = {subtotal:,} تومان",
                    size_hint_y=None,
                    height=45
                ))

        scroll.add_widget(box)
        content.add_widget(scroll)

        content.add_widget(Label(
            text=f"مبلغ کل: {total:,} تومان",
            font_size="20sp",
            size_hint_y=None,
            height=50
        ))

        close = Button(text="بستن", size_hint_y=None, height=50)
        content.add_widget(close)

        popup = Popup(
            title="🛒 سبد خرید",
            content=content,
            size_hint=(0.9, 0.85)
        )
        close.bind(on_press=popup.dismiss)
        popup.open()

    def admin_login(self, instance):
        box = BoxLayout(orientation="vertical", padding=10, spacing=10)

        password = TextInput(
            hint_text="رمز مدیریت",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50
        )
        box.add_widget(password)

        buttons = BoxLayout(size_hint_y=None, height=50, spacing=8)
        login = Button(text="ورود")
        cancel = Button(text="لغو")
        buttons.add_widget(login)
        buttons.add_widget(cancel)
        box.add_widget(buttons)

        popup = Popup(
            title="🔐 ورود به مدیریت",
            content=box,
            size_hint=(0.85, 0.4)
        )

        def check(_):
            if password.text == ADMIN_PASSWORD:
                popup.dismiss()
                self.admin_panel()
            else:
                self.show_message("خطا", "رمز مدیریت اشتباه است.")

        login.bind(on_press=check)
        cancel.bind(on_press=popup.dismiss)
        popup.open()

    def admin_panel(self):
        content = BoxLayout(orientation="vertical", padding=10, spacing=8)

        scroll = ScrollView()
        box = GridLayout(cols=1, spacing=8, size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        for name, price in list(self.products.items()):
            row = BoxLayout(
                size_hint_y=None,
                height=55,
                spacing=5
            )

            edit = Button(
                text=f"{name} | {price:,}",
                size_hint_x=0.65
            )
            delete = Button(
                text="حذف",
                size_hint_x=0.35
            )

            edit.bind(
                on_press=lambda instance, n=name: self.edit_product(n)
            )
            delete.bind(
                on_press=lambda instance, n=name: self.delete_product(n)
            )

            row.add_widget(edit)
            row.add_widget(delete)
            box.add_widget(row)

        scroll.add_widget(box)
        content.add_widget(scroll)

        add = Button(
            text="➕ افزودن کالا",
            size_hint_y=None,
            height=55
        )
        close = Button(
            text="بستن",
            size_hint_y=None,
            height=50
        )

        content.add_widget(add)
        content.add_widget(close)

        popup = Popup(
            title="⚙️ پنل مدیریت",
            content=content,
            size_hint=(0.95, 0.9)
        )

        add.bind(on_press=lambda _: (popup.dismiss(), self.add_product()))
        close.bind(on_press=popup.dismiss)
        popup.open()

    def add_product(self):
        box = BoxLayout(orientation="vertical", padding=10, spacing=8)

        name = TextInput(
            hint_text="نام کالا",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        price = TextInput(
            hint_text="قیمت به تومان",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        box.add_widget(name)
        box.add_widget(price)

        buttons = BoxLayout(size_hint_y=None, height=50, spacing=8)
        save = Button(text="ذخیره")
        cancel = Button(text="لغو")
        buttons.add_widget(save)
        buttons.add_widget(cancel)
        box.add_widget(buttons)

        popup = Popup(
            title="➕ افزودن کالا",
            content=box,
            size_hint=(0.9, 0.55)
        )

        def save_item(_):
            n = name.text.strip()
            try:
                p = int(price.text)
            except ValueError:
                self.show_message("خطا", "قیمت را درست وارد کنید.")
                return

            if not n:
                self.show_message("خطا", "نام کالا را وارد کنید.")
                return

            if p < 0:
                self.show_message("خطا", "قیمت نمی‌تواند منفی باشد.")
                return

            self.products[n] = p
            self.save_products()
            popup.dismiss()
            self.refresh_products()
            self.admin_panel()

        save.bind(on_press=save_item)
        cancel.bind(on_press=popup.dismiss)
        popup.open()

    def edit_product(self, old_name):
        box = BoxLayout(orientation="vertical", padding=10, spacing=8)

        name = TextInput(
            text=old_name,
            multiline=False,
            size_hint_y=None,
            height=50
        )
        price = TextInput(
            text=str(self.products[old_name]),
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        box.add_widget(name)
        box.add_widget(price)

        buttons = BoxLayout(size_hint_y=None, height=50, spacing=8)
        save = Button(text="ذخیره")
        cancel = Button(text="لغو")
        buttons.add_widget(save)
        buttons.add_widget(cancel)
        box.add_widget(buttons)

        popup = Popup(
            title="✏️ ویرایش کالا",
            content=box,
            size_hint=(0.9, 0.55)
        )

        def save_item(_):
            new_name = name.text.strip()

            try:
                new_price = int(price.text)
            except ValueError:
                self.show_message("خطا", "قیمت را درست وارد کنید.")
                return

            if not new_name:
                self.show_message("خطا", "نام کالا را وارد کنید.")
                return

            if new_price < 0:
                self.show_message("خطا", "قیمت نمی‌تواند منفی باشد.")
                return

            if new_name != old_name:
                del self.products[old_name]

            self.products[new_name] = new_price
            self.save_products()
            popup.dismiss()
            self.refresh_products()
            self.admin_panel()

        save.bind(on_press=save_item)
        cancel.bind(on_press=popup.dismiss)
        popup.open()

    def delete_product(self, name):
        box = BoxLayout(orientation="vertical", padding=10, spacing=10)

        box.add_widget(Label(
            text=f"آیا «{name}» حذف شود؟"
        ))

        buttons = BoxLayout(size_hint_y=None, height=50, spacing=8)
        yes = Button(text="بله")
        no = Button(text="خیر")
        buttons.add_widget(yes)
        buttons.add_widget(no)
        box.add_widget(buttons)

        popup = Popup(
            title="حذف کالا",
            content=box,
            size_hint=(0.85, 0.4)
        )

        def remove(_):
            del self.products[name]
            self.cart.pop(name, None)
            self.save_products()
            popup.dismiss()
            self.refresh_products()
            self.admin_panel()

        yes.bind(on_press=remove)
        no.bind(on_press=popup.dismiss)
        popup.open()

    def show_message(self, title, message):
        box = BoxLayout(orientation="vertical", padding=10, spacing=10)

        box.add_widget(Label(text=message))

        close = Button(
            text="باشه",
            size_hint_y=None,
            height=50
        )
        box.add_widget(close)

        popup = Popup(
            title=title,
            content=box,
            size_hint=(0.85, 0.4)
        )
        close.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    RoniyaShop().run()
