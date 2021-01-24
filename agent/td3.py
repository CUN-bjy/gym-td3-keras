'''
MIT License

Copyright (c) 2020 Junyoeb Baek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import numpy as np

from .actor import ActorNet
from .critic import CriticNet

from utils.memory_buffer import MemoryBuffer
from utils.noise_process import OrnsteinUhlenbeckProcess

BUFFER_SIZE = 20000
class td3Agent():
	"""Twin Delayed Deep Deterministic Policy Gradient(TD3) Agent
	"""
	def __init__(self, env_, is_discrete=False, batch_size=100, w_per=True, update_delay=2):
		# gym environments
		self.env = env_
		self.discrete = is_discrete
		self.obs_dim = env_.observation_space.shape[0]
		self.act_dim = env_.action_space.n if is_discrete else env_.action_space.shape[0]

		self.action_bound = (env_.action_space.high - env_.action_space.low) / 2 if not is_discrete else 1.
		self.action_shift = (env_.action_space.high + env_.action_space.low) / 2 if not is_discrete else 0.

		# initialize actor & critic and its targets
		self.discount_factor = 0.99
		self.actor = ActorNet(self.obs_dim, self.act_dim, self.action_bound, lr_=3e-4,tau_=5e-3)
		self.critic = CriticNet(self.obs_dim, self.act_dim, lr_=3e-4,tau_=5e-3,discount_factor=self.discount_factor)

		# Experience Buffer
		self.buffer = MemoryBuffer(BUFFER_SIZE, with_per=w_per)
		self.with_per = w_per
		self.batch_size = batch_size

		# for Delayed Policy Update
		self._update_step = 0
		self._target_update_interval = update_delay

	###################################################
	# Network Related
	###################################################
	def make_action(self, obs, noise=True):
		""" predict next action from Actor's Policy
		"""
		action_ = self.actor.predict(obs)[0]; sigma=0.1 # std of gaussian
		a = np.clip(action_ + np.random.normal(0,self.action_bound*sigma) if noise else 0, -self.action_bound, self.action_bound)
		return a

	def make_target_action(self, obs, noise=True):
		""" predict next action from Actor's Target Policy
		"""
		action_ = self.actor.target_predict(obs); sigma=0.2
		cliped_noise = np.clip(np.random.normal(0,self.action_bound*sigma),-self.action_bound*0.5,self.action_bound*0.5)
		a = np.clip(action_ + cliped_noise if noise else 0, -self.action_bound, self.action_bound)
		return a

	def update_networks(self, obs, acts, critic_target):
		""" Train actor & critic from sampled experience
		"""
		# update critic
		self.critic.train(obs, acts, critic_target)

		if self._update_step % self._target_update_interval == 0:
			print("Policy Update!")
			# update actor
			self.actor.train(obs,self.critic.network_1)

			# update target networks
			self.actor.target_update()
			self.critic.target_update()
		self._update_step = self._update_step + 1

	def replay(self):
		if self.with_per and (self.buffer.size() <= self.batch_size): return

		# sample from buffer
		states, actions, rewards, dones, new_states, idx = self.sample_batch(self.batch_size)

		# get target q-value using target network
		new_actions = self.make_target_action(new_states)
		q1_vals = self.critic.target_network_1.predict([new_states, new_actions])
		q2_vals = self.critic.target_network_2.predict([new_states, new_actions])

		# bellman iteration for target critic value
		q_vals = np.min(np.vstack([q1_vals.transpose(),q2_vals.transpose()]),axis=0)
		critic_target = np.asarray(q_vals)
		# print(np.vstack([q1_vals.transpose(),q2_vals.transpose()]))
		# print(q_vals)
		for i in range(q1_vals.shape[0]):
			if dones[i]:
				critic_target[i] = rewards[i]
			else:
				critic_target[i] = self.discount_factor * q_vals[i] + rewards[i]

			if self.with_per:
				self.buffer.update(idx[i], abs(q_vals[i]-critic_target[i]))

		# train(or update) the actor & critic and target networks
		self.update_networks(states, actions, critic_target)


	####################################################
	# Buffer Related
	####################################################

	def memorize(self,obs,act,reward,done,new_obs):
		"""store experience in the buffer
		"""
		if self.with_per:
			# not implemented for td3, yet.
			q_val = self.critic.network([np.expand_dims(obs,axis=0),self.actor.predict(obs)])
			next_action = self.actor.target_network.predict(np.expand_dims(new_obs, axis=0))
			q_val_t = self.critic.target_network.predict([np.expand_dims(new_obs,axis=0), next_action])
			new_val = reward + self.discount_factor * q_val_t
			td_error = abs(new_val - q_val)[0]
		else:
			td_error = 0			

		self.buffer.memorize(obs,act,reward,done,new_obs,td_error)

	def sample_batch(self, batch_size):
		""" Sampling from the batch
		"""
		return self.buffer.sample_batch(batch_size)

	###################################################
	# Save & Load Networks
	###################################################
	def save_weights(self,path):
		""" Agent's Weights Saver
		"""
		self.actor.save_network(path)
		self.critic.save_network(path)

	def load_weights(self, pretrained):
		""" Agent's Weights Loader
		"""
		self.actor.load_network(pretrained)
		self.critic.load_network(pretrained)