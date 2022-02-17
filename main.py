import yaml

world_guard_yml = "/home/alexander/Taygiria/test/worlds/world_the_end/regions.yml"

ignore_regions = ["__global__"]

saved_mca_files = set()

with open(world_guard_yml, 'r') as f:
    templates = yaml.safe_load(f)

    if templates.get('regions'):
        for rg, rg_value in templates.get('regions').items():
            if rg not in ignore_regions:
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

for file in saved_mca_files:
    print(file)