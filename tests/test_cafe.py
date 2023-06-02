from app import schemas
import pytest


def test_get_all_cafes(authorized_client, test_cafes):
    res = authorized_client.get("/cafes/")

    def validate(cafe):
        return schemas.Cafe(**cafe)

    cafes_map = map(validate, res.json())
    cafes_list = list(cafes_map)

    assert len(res.json()) == len(test_cafes)
    assert res.status_code == 200


def test_unauthorized_user_get_all_cafes(client, test_cafes):
    res = client.get("/cafes/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_cafes(client, test_cafes):
    res = client.get(f"/cafes/{test_cafes[0].id}")
    assert res.status_code == 401


def test_get_one_cafe_not_exist(authorized_client, test_cafes):
    res = authorized_client.get(f"/posts/888888")
    assert res.status_code == 404


def test_get_one_cafe(authorized_client, test_cafes):
    res = authorized_client.get(f"/cafes/{test_cafes[0].id}")
    cafe = schemas.Cafe(**res.json())
    assert cafe.id == test_cafes[0].id
    assert cafe.name == test_cafes[0].name
    assert cafe.location == test_cafes[0].location


@pytest.mark.parametrize("name, location, can_take_calls, coffee_price, has_sockets, has_wifi, map_url, seats", [
    ("chai sutta bar", "bhopal", True, 20, True, True, "bhopal", 25),
    ("Fantasy", "bhopal", True, 25, True, True, "bhopal", 30),
    ("Tinku's", "bhopal", True, 20, True, True, "bhopal", 40)
])
def test_create_cafe(authorized_client, test_user, test_cafes, name, location, can_take_calls, coffee_price, has_sockets, has_wifi, map_url, seats):
    res = authorized_client.post(
        "/cafes/", json={"name": name,
                         "location": location,
                         "can_take_calls": can_take_calls,
                         "coffee_price": coffee_price,
                         "has_sockets": has_sockets,
                         "has_wifi": has_wifi,
                         "map_url": map_url,
                         "seats": seats
                         }
    )
    print(res.json())
    created_cafe = schemas.Cafe(**res.json())
    assert res.status_code == 201
    assert created_cafe.name == name
    assert created_cafe.location == location
    assert created_cafe.can_take_calls == can_take_calls
    assert created_cafe.owner_id == test_user['id']


def test_unauthorized_user_create_cafe(client, test_user, test_cafes):
    res = client.post(
        "/cafes/", json={"name": "demo",
                         "location": "demo",
                         "can_take_calls": True,
                         "coffee_price": 20,
                         "has_sockets": True,
                         "has_wifi": True,
                         "map_url": "demo",
                         "seats": 20
                         }
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_cafe(client, test_user, test_cafes):
    res = client.delete(
        f"/cafes/{test_cafes[0].id}"
    )
    assert res.status_code == 401


def test_delete_cafe_success(authorized_client, test_user, test_cafes):
    res = authorized_client.delete(
        f"/cafes/{test_cafes[0].id}"
    )
    assert res.status_code == 204


def test_delete_cafe_non_exist(authorized_client, test_user, test_cafes):
    res = authorized_client.delete(
        "/cafes/80000"
    )
    assert res.status_code == 404


def test_delete_other_user_cafe(authorized_client, test_user, test_cafes):
    res = authorized_client.delete(
        f"/cafes/{test_cafes[2].id}"
    )
    assert res.status_code == 403


def test_update_cafe(authorized_client, test_user, test_cafes):
    data = {
        "name": "demo",
        "location": "demo",
        "can_take_calls": True,
        "coffee_price": 20,
        "has_sockets": True,
        "has_wifi": True,
        "map_url": "demo",
        "seats": 20
    }
    res = authorized_client.put(f"/cafes/{test_cafes[0].id}", json=data)
    updated_cafe = schemas.Cafe(**res.json())
    assert res.status_code == 200
    assert updated_cafe.name == data['name']
    assert updated_cafe.location == data['location']


def test_update_other_user_cafe(authorized_client, test_user, test_cafes, test_user2):
    data = {
        "name": "updated name",
        "location": "updated location",
        "can_take_calls": True,
        "coffee_price": 20,
        "has_sockets": True,
        "has_wifi": True,
        "map_url": "updated url",
        "seats": 20
    }
    res = authorized_client.put(f"/cafes/{test_cafes[2].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_cafe(client, test_user, test_cafes):
    res = client.put(
        f"/cafes/{test_cafes[0].id}"
    )
    assert res.status_code == 401


def test_update_cafe_non_exist(authorized_client, test_user, test_cafes):
    data = {
        "name": "updated name",
        "location": "updated location",
        "can_take_calls": True,
        "coffee_price": 20,
        "has_sockets": True,
        "has_wifi": True,
        "map_url": "updated url",
        "seats": 20
    }

    res = authorized_client.put(
        f"/cafes/80000", json=data
    )

    assert res.status_code == 404
