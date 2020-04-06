import asyncio
import aiojobs
import conf
import requests
from Package import Package
from aiochannel import Channel
from bs4 import BeautifulSoup
from meili_index import get_or_create_meilisearch_index, index_packages


def get_url_list():

    print("Retrieving pkg list")
    pkg_list_response = requests.get(conf.SIMPLE_API_URL)
    soup = BeautifulSoup(pkg_list_response.text, "html.parser")
    all_pkg_list = soup.find_all('a')[conf.pkg_list_offset:]
    print("Pkg list retrieved. {} items.".format(len(all_pkg_list)))
    return all_pkg_list


async def single_pkg_req(pkg, channel):

    try:
        await pkg.update_pypi_data()
        await channel.put(pkg)
    except Exception as e:
        print(e)


async def main():

    all_pkg = []
    indexed_counter = 0

    # Create a Meilisearch index
    index = get_or_create_meilisearch_index()
    if index is None:
        exit("ERROR: Couldn't create a Meilisearch index")

    channel = Channel(loop=asyncio.get_event_loop())
    pkg_list = get_url_list()
    scheduler = await aiojobs.create_scheduler()
    scheduler._limit = conf.pkg_indexing_batch_size
    for pkg_link in pkg_list:
        pkg = Package(pkg_link.get_text())
        await scheduler.spawn(single_pkg_req(pkg, channel))
    async for pkg in channel:
        all_pkg.append(pkg)
        if len(all_pkg) >= conf.pkg_indexing_batch_size:
            batch = all_pkg[:conf.pkg_indexing_batch_size]
            all_pkg = all_pkg[conf.pkg_indexing_batch_size:]
            indexed_counter += index_packages(batch, index)
            print("Packages treated: {}".format(indexed_counter))
asyncio.get_event_loop().run_until_complete(main())

# https://github.com/Kerollmops/meili-crates/blob/master/src/bin/full_update.rs#L12-L40
# https://github.com/aio-libs/aiohttp/blob/master/examples/client_json.py
# https://github.com/tbug/aiochannel
# https://github.com/aio-libs/aiojobs
# https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor
