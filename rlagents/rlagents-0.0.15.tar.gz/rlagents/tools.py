from multiprocessing import Pool
import random
import types
import os


runid_size = 200
base_reporting_path = 'DataDir'


def record_everything(*args):
    return [str(i) for i in args]


def run_n_episodes(args):
    agent, env, n_episodes, max_steps, trial_number, episode_callback = args
    runid = str(random.getrandbits(runid_size))
    agent.reset()
    data = []
    measure_episode = False
    agent_ep = float(agent.ep)
    for episode in range(n_episodes*2):  # Because we train and test together
        episode //= 2  # Count every other episode
        agent.ep = 1 if measure_episode else agent_ep
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
        if measure_episode:
            data.append(episode_callback(runid, agent, env, episode,
                                         totalrew, trial_number))
        measure_episode = not measure_episode
    path = os.path.join(base_reporting_path, runid)
    # Restore original ep
    agent.ep = agent_ep

    try:
        import ujson as json
    except:
        import json
    with open(path, 'w') as fl:
        json.dump(data, fl)
    return path


def benchmark(agent_list, env_list, n_episodes,
              max_steps_per_episode, n_trials):

    from tqdm import tqdm
    if not os.path.exists(base_reporting_path):
        print('{} does not exist. Creating...'.format(base_reporting_path))
        os.mkdir(base_reporting_path)
    else:
        print('{} Exists'.format(base_reporting_path))

    if max_steps_per_episode is None:
        max_steps_per_episode = int(1e10)
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
