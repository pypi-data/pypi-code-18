from multiprocessing import Pool
import random
import types
import os
try:
    import ujson as json
except:
    import json


runid_size = 200
base_reporting_path = 'DataDir'
hard_step_limit = int(1e10)


def record_everything(*args):
    return [str(i) for i in args]


def run_n_episodes(args):
    (agent, env, n_episodes, max_steps,
     trial_number, episode_callback, train_steps) = args
    runid = str(random.getrandbits(runid_size))
    agent.reset()
    data = []
    agent_ep = float(agent.ep)
    for episode in range(n_episodes):
        if episode % train_steps == 0:
            agent.ep = 1
        obs = env.reset()
        totalrew = 0
        agent.start_episode()
        for step in range(max_steps):
            act = agent.get_action(obs)
            obs, rew, done, info = env.step(act)
            agent.observe_reward(rew)
            if not isinstance(rew, (float, int)):
                rew = sum(rew)
            totalrew += rew
            if done:
                break
        agent.end_episode()
        if episode % train_steps == 0:
            data.append(episode_callback(runid, agent, env, episode,
                                         totalrew, trial_number))
            agent.ep = agent_ep
    path = os.path.join(base_reporting_path, runid)
    # Make sure to restore original ep
    agent.ep = agent_ep

    with open(path, 'w') as fl:
        json.dump(data, fl)
    return path


def benchmark(agent_list, env_list, n_episodes,
              max_steps_per_episode, n_trials, train_steps=2):
    from tqdm import tqdm
    if not os.path.exists(base_reporting_path):
        print('{} does not exist. Creating...'.format(base_reporting_path))
        os.mkdir(base_reporting_path)
        already_done = 0
    else:
        message = '{} Exists. Continuing experiment...'
        print(message.format(base_reporting_path))
        already_done = len(os.listdir(base_reporting_path))
    if max_steps_per_episode is None:
        max_steps_per_episode = hard_step_limit
    print('Building Dispatch list...')
    arguments = [(agent.copy(), env.copy(), n_episodes, max_steps_per_episode,
                  trial_index+already_done, record_everything, train_steps)
                 for agent in agent_list
                 for env in env_list
                 for trial_index in range(n_trials)]
    # Stoping at any time should not give you data biased to some agent-world
    random.shuffle(arguments)
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


def parse(d):
    return (None,
            'Q-Learning' if 'Q' in d[1] else 'Generalized Learning',
            None,
            int(d[3]),
            float(d[4]),
            int(d[5]))


def readfile(path):
    with open(path, 'r') as fl:
        da = json.load(fl)
        x = list(map(parse, da))
    return x


def make_df(paths):
    from tqdm import tqdm
    import pandas as pd
    print('{} files'.format(len(paths)))
    print('Reading files...')
    with Pool() as pool:
        filepaths = paths
        work = pool.imap_unordered(readfile, filepaths)
        data = []
        for d in tqdm(work, total=len(filepaths), ncols=80, leave=False):
            data.extend(d)
    print('Painting...')
    data = pd.DataFrame(data, columns=['runid', 'agent',
                                       'world', 'ep',
                                       'rew', 'trial'])
    return data
