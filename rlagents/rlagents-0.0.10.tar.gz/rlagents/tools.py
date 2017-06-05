from multiprocessing import Pool
from tqdm import tqdm
import random
import ujson
import types
import os


runid_size = 200
base_reporting_path = 'DataDir'


def record_everything(*args):
    return args


def run_n_episodes(args):
    agent, env, n_episodes, max_steps, trial_number, episode_callback = args
    runid = str(random.getrandbits(runid_size))
    agent.reset()
    data = []
    for episode in range(n_episodes):
        obs = env.reset()
        totalrew = 0
        agent.start_episode()
        for step in range(max_steps):
            act = agent.get_action(obs)
            obs, rew, done, info = env.step(act)
            agent.observe_reward(rew)
            totalrew += rew
            if done:
                break
        agent.end_episode()
        data.append(episode_callback(runid, agent, env, episode,
                                     totalrew, trial_number))
    path = os.path.join(base_reporting_path, runid)
    with open(path, 'w') as fl:
        ujson.dump(data, fl)
    return path


def benchmark(agent_list, env_list, n_episodes,
              max_steps_per_episode, n_trials):
    if not os.path.exists(base_reporting_path):
        print('{} does not exist. Creating...'.format(base_reporting_path))
        os.mkdir(base_reporting_path)
    else:
        print('{} Exists'.format(base_reporting_path))

    print('Building Dispatch list...')
    arguments = [(agent.copy(), env.copy(), n_episodes, max_steps_per_episode,
                  trial_index, record_everything)
                 for agent in agent_list
                 for env in env_list
                 for trial_index in range(n_trials)]
    print('Running experiments...')
    paths = []
    try:
        with Pool() as pool:
            work = pool.imap_unordered(run_n_episodes, arguments)
            for datapath in tqdm(work, total=len(arguments)):
                paths.append(datapath)
    except KeyboardInterrupt:
        print('Stopping Experiments...')
    else:
        print('Experiments completed...')
    return paths


def gymwrapper(env):
    "Return an env which can copy()"
    def envcloner(self):
        import gym
        return gym.make(self.spec.id)
    env.copy = types.MethodType(envcloner, env)
    return env
