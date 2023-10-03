#!/usr/bin/env python3
import yaml
import argparse

ignore_regions = ["__global__"]


def generate_mca(world_guard_yml: str, required_region: str = ""):
    saved_mca_files = set()

    with open(world_guard_yml, 'r') as f:
        templates = yaml.safe_load(f)

        if templates.get('regions'):
            for rg, rg_value in templates.get('regions').items():
                if required_region == "" and rg in ignore_regions:
                    continue
                if required_region != "" and rg != required_region:
                    continue

                start_x = rg_value.get('min').get('x')
                start_z = rg_value.get('min').get('z')
                end_x = rg_value.get('max').get('x')
                end_z = rg_value.get('max').get('z')

                summer_x = 1 if start_x < end_x else -1
                summer_z = 1 if start_z < end_z else -1

                start_mc_x = start_x // 512
                start_mc_z = start_z // 512

                end_mc_x = end_x // 512
                end_mc_z = end_z // 512

                for x in range(start_mc_x, end_mc_x + 1) if summer_x > 0 else range(end_mc_x, start_mc_x + 1):
                    for z in range(start_mc_z, end_mc_z + 1) if summer_z > 0 else range(end_mc_z, start_mc_z + 1):
                        file_name = "r.{}.{}.mca".format(x, z)
                        saved_mca_files.add(file_name)

    return saved_mca_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Калькулятор .mca файлов по списку регионов WorldGuard')

    parser.add_argument("-w", "--worldguard-regions", help="Файл с регионами WorldGuard", required=True)
    parser.add_argument("-n", "--name-region", help="Навзвание региона региона, если нужен только один регион", required=False)

    args = parser.parse_args()

    args.name_region = args.name_region.lower()

    try:
        for file in generate_mca(args.worldguard_regions, args.name_region):
            print(file)
    except FileNotFoundError:
        print("Файл не найден: ", args.worldguard_regions)
    except PermissionError:
        print("Permission denied: ", args.worldguard_regions)
