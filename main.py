from web_search import PhantomShark, User
from web_search.search.SixSoft.six_soft import SixSoft
from web_search.search.SkyGrass.sky_grass import SkyGrass


if __name__ == "__main__":
    search_key = "test"

    shark_user = User("ATM666888", "ATM666888")
    shark = PhantomShark(user=shark_user)
    shark_data = shark.search(search_key)
    print(shark_data)

    sixsoft_user = User("zyb666", "a123456789")
    sixsoft = SixSoft(user=sixsoft_user)
    sixsoft_data = sixsoft.search(search_key)
    print(sixsoft_data)

    skygrass_user = User("hm010", "010010")
    skygrass = SkyGrass(user=skygrass_user)
    skygrass_data = skygrass.search(search_key)

    print(skygrass_data)
