import pytest
from praktikum.burger import Burger


class TestBurger:
    def test_set_buns(self, bun_factory):
        b = Burger()
        bun = bun_factory(name="black bun", price=150.0)
        b.set_buns(bun)
        assert b.bun is bun

    def test_add_ingredient(self, burger, ingredient_factory):
        ing = ingredient_factory("FILLING", "Cutlet", 50.0)
        burger.add_ingredient(ing)
        assert burger.ingredients == [ing]

    def test_remove_ingredient(self, burger, ingredient_factory):
        a = ingredient_factory("SAUCE", "A", 5.0)
        b = ingredient_factory("FILLING", "B", 6.0)
        c = ingredient_factory("SAUCE", "C", 7.0)
        burger.add_ingredient(a)
        burger.add_ingredient(b)
        burger.add_ingredient(c)

        burger.remove_ingredient(1)

        assert burger.ingredients == [a, c]

    @pytest.mark.parametrize(
        "names, src, dst, expected",
        [
            (["A", "B", "C", "D"], 0, 3, ["B", "C", "D", "A"]),
            (["A", "B", "C"], 2, 0, ["C", "A", "B"]),
            (["A", "B"], 1, 1, ["A", "B"]),
        ],
    )
    def test_move_ingredient(self, burger, ingredient_factory, names, src, dst, expected):
        for n in names:
            burger.add_ingredient(ingredient_factory("SAUCE", n, 1.0))

        burger.move_ingredient(src, dst)

        got = [i.get_name() for i in burger.ingredients]
        assert got == expected

    @pytest.mark.parametrize(
        "bun_price, prices, expected",
        [
            (100.0, [], 200.0),
            (120.0, [10.0], 120.0 * 2 + 10.0),
            (0.0, [0.0, 0.0], 0.0),
            (199.99, [1.01, 2.02, 3.03], 199.99 * 2 + 1.01 + 2.02 + 3.03),
        ],
    )
    def test_get_price(self, bun_factory, ingredient_factory, bun_price, prices, expected):
        b = Burger()
        b.set_buns(bun_factory(price=bun_price))
        for i, p in enumerate(prices):
            t = "SAUCE" if i % 2 == 0 else "FILLING"
            b.add_ingredient(ingredient_factory(t, f"i{i}", p))

        assert b.get_price() == pytest.approx(expected)

    def test_get_receipt(self, bun_factory, ingredient_factory):
        b = Burger()
        b.set_buns(bun_factory(name="white bun", price=200.0))

        i1 = ingredient_factory("SAUCE", "Sour Cream", 20.0)
        i2 = ingredient_factory("FILLING", "Cutlet", 50.0)
        i3 = ingredient_factory("SAUCE", "Chili", 30.0)

        b.add_ingredient(i1)
        b.add_ingredient(i2)
        b.add_ingredient(i3)

        b.move_ingredient(2, 1)  
        b.remove_ingredient(2)   

        expected_total = 200.0 * 2 + 20.0 + 30.0
        expected_text = "\n".join(
            [
                "(==== white bun ====)",
                "= sauce Sour Cream =",
                "= sauce Chili =",
                "(==== white bun ====)\n",
                f"Price: {expected_total}",
            ]
        )

        assert b.get_receipt() == expected_text
