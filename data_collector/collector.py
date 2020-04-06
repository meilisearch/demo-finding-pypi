import asyncio
import aiojobs
import conf
from pypi import pypi
from aiochannel import Channel
from meili import meili_index as meili


async def handle_package_loop(channel, pkg_list_size, index):

    all_pkg = []
    indexed_counter = 0

    pkg_count = 0
    async for pkg in channel:
        pkg_count += 1
        if pkg is not None:
            all_pkg.append(pkg)

        # Handle a batch
        if len(all_pkg) >= conf.pkg_indexing_batch_size:
            batch = all_pkg[:conf.pkg_indexing_batch_size]
            all_pkg = all_pkg[conf.pkg_indexing_batch_size:]
            indexed_counter += meili.index_packages(batch, index)
            print("{}: {}".format(
                "Total packages sent to MeiliSearch Index",
                indexed_counter
            ))

        # Handle last batch
        elif pkg_count == pkg_list_size \
                or (conf.pkg_cnt_limit and pkg_count >= conf.pkg_cnt_limit):
            indexed_counter += meili.index_packages(all_pkg, index)
            print("{}: {}".format(
                "Total packages sent to MeiliSearch Index",
                indexed_counter
            ))
            channel.close()
            break



async def main():

    # Create a Meilisearch index
    index = meili.get_or_create_index()
    if index is None:
        exit("\tERROR: Couldn't create a Meilisearch index")

    # Create a Create an Asynchronous scheduler and channel
    scheduler = await aiojobs.create_scheduler()
    scheduler._limit = conf.pkg_indexing_batch_size
    channel = Channel(loop=asyncio.get_event_loop())

    pkg_list = pypi.get_url_list()
    await scheduler.spawn(handle_package_loop(channel, len(pkg_list), index))
    for pkg_link in pkg_list:
        pkg = pypi.Package(pkg_link.get_text())
        await scheduler.spawn(pkg.single_pkg_request(channel))
    await channel.join()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
