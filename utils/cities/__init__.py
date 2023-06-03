import os
import pandas as pd
import pinyin
root = os.path.dirname(os.path.realpath(__file__))

cities_code = pd.read_csv(
    os.path.join(root, "mainland_adcode.csv"), engine="python", encoding="utf-8-sig"
)


def name2code(name):
    name = name.replace("城区", "")
    name = name.replace("郊县", "")
    try:
        name_filter = cities_code["NAME"].apply(lambda x: name in x)
        return str(cities_code[name_filter]["CITYADCODE"].item())
    except:
        try:
            name_filter = cities_code["NAME"].apply(
                lambda x: name
                in pinyin.get(x, format="strip", delimiter="")[: len(name)]
            )
            return str(cities_code[name_filter]["CITYADCODE"].item())
        except:
            try:
                name_map = {"xiamen": "厦门", "chongqing": "重庆", "xian": "西安"}
                if name in name_map.keys():
                    return name2code(name_map[name])
                elif name == "fuzhou":
                    print("fuzhou 默认福州，抚州请输入中文")
                    return name2code("福州")
                elif name == "suzhou":
                    print("suzhou 默认苏州，其它请输入中文")
                    return name2code("苏州")
                else:
                    print("cannot find", name)
                    return None
            except:
                print("cannot find", name)
                return None


def code2name(code):
    try:
        return cities_code[cities_code["CITYADCODE"] == int(code)]["NAME"].item()
    except:
        print("cannot find ", code)
        return None


if __name__ == "__main__":
    print(name2code("广州"))
    # print(code2name(540100))
