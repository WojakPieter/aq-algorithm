from aq import Example, AQ, Rule


def main():
    xnLabels = {
        "aura": ["sloneczna", "pochmurna", "deszczowa"],
        "temperatura": ["ciepla", "umiarkowana", "zimna"],
        "wilgotnosc": ["duza", "normalna"],
        "wiatr": ["slaby", "silny"],
    }
    x1 = Example(
        xnLabels,
        {
            "aura": "sloneczna",
            "temperatura": "ciepla",
            "wilgotnosc": "duza",
            "wiatr": "slaby",
        },
        0,
    )
    x2 = Example(
        xnLabels,
        {
            "aura": "sloneczna",
            "temperatura": "ciepla",
            "wilgotnosc": "duza",
            "wiatr": "silny",
        },
        0,
    )
    x3 = Example(
        xnLabels,
        {
            "aura": "pochmurna",
            "temperatura": "ciepla",
            "wilgotnosc": "duza",
            "wiatr": "slaby",
        },
        1,
    )
    x4 = Example(
        xnLabels,
        {
            "aura": "deszczowa",
            "temperatura": "umiarkowana",
            "wilgotnosc": "duza",
            "wiatr": "slaby",
        },
        1,
    )
    x5 = Example(
        xnLabels,
        {
            "aura": "deszczowa",
            "temperatura": "zimna",
            "wilgotnosc": "normalna",
            "wiatr": "slaby",
        },
        1,
    )
    x6 = Example(
        xnLabels,
        {
            "aura": "deszczowa",
            "temperatura": "zimna",
            "wilgotnosc": "normalna",
            "wiatr": "silny",
        },
        0,
    )
    x7 = Example(
        xnLabels,
        {
            "aura": "pochmurna",
            "temperatura": "zimna",
            "wilgotnosc": "normalna",
            "wiatr": "silny",
        },
        1,
    )
    x8 = Example(
        xnLabels,
        {
            "aura": "sloneczna",
            "temperatura": "umiarkowana",
            "wilgotnosc": "duza",
            "wiatr": "slaby",
        },
        0,
    )
    x9 = Example(
        xnLabels,
        {
            "aura": "sloneczna",
            "temperatura": "zimna",
            "wilgotnosc": "normalna",
            "wiatr": "slaby",
        },
        1,
    )
    x10 = Example(
        xnLabels,
        {
            "aura": "deszczowa",
            "temperatura": "umiarkowana",
            "wilgotnosc": "normalna",
            "wiatr": "slaby",
        },
        1,
    )
    x11 = Example(
        xnLabels,
        {
            "aura": "sloneczna",
            "temperatura": "umiarkowana",
            "wilgotnosc": "normalna",
            "wiatr": "silny",
        },
        1,
    )
    x12 = Example(
        xnLabels,
        {
            "aura": "pochmurna",
            "temperatura": "umiarkowana",
            "wilgotnosc": "duza",
            "wiatr": "silny",
        },
        1,
    )
    x13 = Example(
        xnLabels,
        {
            "aura": "pochmurna",
            "temperatura": "ciepla",
            "wilgotnosc": "normalna",
            "wiatr": "slaby",
        },
        1,
    )
    x14 = Example(
        xnLabels,
        {
            "aura": "deszczowa",
            "temperatura": "umiarkowana",
            "wilgotnosc": "duza",
            "wiatr": "silny",
        },
        0,
    )

    data = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14]
    aq = AQ(data, xnLabels, 1, "ordered", [], False, True)
    aq.run()

    [print(rule) for rule in aq.rules]


if __name__ == "__main__":
    main()
