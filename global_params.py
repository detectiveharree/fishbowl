from items.itemresources.itemresource import GROUP_BUFFER_FACTOR

# param for how many ticks in a day
daily_ticks = 288
hourly_ticks = int(daily_ticks / 24)


# param for how many days stockpiles will be supplied for
supply_days = 10

# params that determine by what amount hunger and thirst increase by each tick
hunger_tick = 0.2
thirst_tick = 0.2
tired_tick = 0.66

starvation_death_threshold = 14 * daily_ticks * hunger_tick # die if not eat for 14 days
dehydration_death_threshold = 7 * daily_ticks * thirst_tick # die if not drink for 14 days

food_water_ratio = starvation_death_threshold / dehydration_death_threshold # useful metric


default_group_task_loyalty_threshold = 3 * daily_ticks # willing to work for 3 days straight

# rate tired ness decreases when asleep.
# this is good value for now i.e. sleeps 8 hours awake 16
tired_rejuvination_rate = 2
stamina_rejuvination_rate = 5
health_rejuvination_rate = 1

# 15 hours awake
go_to_sleep_threshold = hourly_ticks * 16
print(go_to_sleep_threshold)
socialise_threshold = 999

inventory_size = 100

incapacitated_health = 0
signal_need_level = 100000

minimum_stockpile_move_distance = 1

group_colour_palette = [(255.0, 0.0, 255.0), (0.0, 127.5, 255.0), (255.0, 127.5, 0.0), (127.5, 191.25, 127.5), (107.96121242028391, 30.091169834987767, 150.99884802039563), (1.6049915112350055, 129.94365854905132, 41.15689584175118), (178.45177502199624, 9.371561025871374, 1.533479914702967), (194.513328061904, 122.88390323645575, 249.45726044219185), (254.13304300530032, 251.0326127570456, 64.74015412771435), (0.0, 255.0, 255.0), (0.0, 0.0, 255.0), (0.0, 255.0, 127.5), (235.1111691864905, 61.84953943038894, 109.30731320440287), (133.97331039683064, 128.01606039039913, 8.910414507821152), (122.47678238465677, 222.07079058829095, 253.89244235210668), (139.78896225470652, 241.78891362912796, 21.526491193347972), (253.38682006925157, 164.66517737462698, 143.12093860899398), (0.9881420690982434, 72.19863487132478, 124.94225651214533), (138.66545078905176, 3.0480873703950495, 254.70620258377426), (16.401340715281236, 159.22283272069592, 150.78097639159375), (84.22967719145241, 60.529468950366564, 51.79698466975781), (99.02164927610485, 109.74451344544171, 215.81851665876388), (191.34585664790617, 247.14645330214842, 160.3282221712317), (164.39906377620844, 111.20428347531998, 123.71554289765243), (187.17463710161505, 56.43467985536776, 199.3363618244789), (197.61312721125665, 182.0435862416129, 14.297158222132826), (18.163524778407652, 205.56365030545342, 62.0786065839377), (37.7901246458063, 0.08648298509938035, 86.5816560206208), (216.14057753658895, 192.93008278567095, 247.43306299046662), (13.822131440023192, 19.714922247886385, 178.19616180692938), (65.05502690925597, 229.20628596523915, 182.9221278208893), (185.28556150811096, 0.44484249235754225, 118.06859179031366), (65.62617780218238, 173.02424354836813, 232.49768944268135), (76.13047571582867, 113.10322572465766, 115.59072544711951), (50.537419012504266, 56.15800038682277, 238.58793151974695)]

min_days_between_group_switch_attempt = 2

TRAVERSABLE_FLAG = 1000
UNCLAIMED_TERRITORY_FLAG = 1000 # must be less then 10000

# default efficiency for other buffer factors
DEFAULT_BUFFER_FACTOR = 1
"""
In absence of information, we will assume by default that the efficiency for getting food and water
is really low. 
"""
DEFAULT_SURVIVAL_BUFFER_FACTOR = 200

