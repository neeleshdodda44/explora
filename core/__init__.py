from ipywidgets import widgets
from IPython.display import display, Image
from core.category_component import CategoryComponent
from core.db_client import DBClient
import pandas as pd
from core.ed_component import EDComponent
import numpy as np

OPTIONS = ['histogram', 'scatter', 'compare using scatter', 'describe','compare using describe']

class Orchestrator(object):
	"""
	Orchestrator Class

	- 
	""" 
	def __init__(self):
		"""
		Initialize Orchestrator instance.
		"""
		self.db_client = DBClient()
		self.category_component = CategoryComponent(db_client)
		self.ed_component = EDComponent()
		self.ed_datasets = list()
		self.method = None
		self.dataset1 = None
		self.dataset2 = None
		self.column1 = None
		self.column2 = None
 
	def get_ed_datasets(self):
		"""
		Returns ed_datasets to the user,
		this is a list.
		"""
		try:
			return self.ed_datasets
		except Exception as inst:
			print(inst)

	def get_dataset_dictionary(self, dataset_index):
		"""
		Returns a dictionary in ed_datasets to the user.

		@param integer dataset_index: index of corresponding directory
		"""
		try:
			return self.ed_datasets[dataset_index]
		except Exception as inst:
			print(inst)

	def category_name(self):
		"""
		Displays:
			Prompt to get category from user.
		"""
		def orchestrate(sender):
			"""
			This method is triggered by the button.on_click event
	    	It uses the current value of category_widget variable
	    	to get the dictionary with ed and stores the value in
	    	a global var.
			"""
			sender.disabled = True
			category_text = category_widget.value.strip().lower()
			cc_dict = self.category_component.get_ed_with_category(category_text)
			# TODO: change this to the actual value of the dictionary, it should not be jsut the category text
			self.ed_datasets = None
			sender.disabled = False


		category_widget = widgets.Text(
			value=None,
			placeholder='',
			description='Category:',
			disabled=False,

		)
		button = widgets.Button(description='Submit')
		display(category_widget)
		display(button)
		button.on_click(orchestrate)

	def visualization_parameters(self):
			"""
			Displays:
				Prompt to get visualization information from user. 
				(Only for directories)
			"""
			def store(sender):
				"""
				
				"""
				sender.disabled = True
				self.method = method_widget.value.strip()
				self.dataset1 = dataset1_widget.value.strip()
				self.dataset2 = dataset2_widget.value.strip()
				self.column1 = column1_widget.value.strip()
				self.column2 = column2_widget.value.strip()
				sender.disabled = False

			dataset1_widget = widgets.Text(
				value=None,
				placeholder='',
				description='Dataset 1:',
				disabled=False,

			)
			dataset2_widget = widgets.Text(
				value=None,
				placeholder='',
				description='Dataset 2:',
				disabled=False,

			)
			column1_widget = widgets.Text(
				value=None,
				placeholder='',
				description='Column 1:',
				disabled=False,

			)
			column2_widget = widgets.Text(
				value=None,
				placeholder='',
				description='Column 2:',
				disabled=False,

			)
			method_widget = widgets.RadioButtons(
			    options=OPTIONS,
			    value='histogram',
			    description='Method:',
			    disabled=False
			)
			button = widgets.Button(description='Submit')

			display(method_widget)
			display(dataset1_widget)
			display(dataset2_widget)
			display(column1_widget)
			display(column2_widget)
			display(button)
			button.on_click(store)

	def visualize(self): 
		"""
		Returns the corresponding plot.
		"""
		try: 
			if (self.method == OPTIONS[0]):
				validate_ed_dataset(self.dataset1)

				dataset1_dict = self.ed_datasets[self.dataset1]
				dataset1_key = list(dataset1_dict.keys())
				dataset1_json = dataset1_dict.get(dataset1_key[0])[1]
				df = pd.read_json(dataset1_json)

				validate_column(df, self.column1)
				return self.ed_component.histogram(df, self.column1)
			elif (self.method == OPTIONS[1]):
				validate_ed_dataset(self.dataset1)

				dataset1_dict = self.ed_datasets[self.dataset1]
				dataset1_key = list(dataset1_dict.keys())
				dataset1_json = dataset1_dict.get(dataset1_key[0])[1]
				df = pd.read_json(dataset1_json)
				
				validate_column(df, self.column1)
				validate_column(df, self.column2)
				return self.ed_component.scatter(df, self.column1, self.column2)
			elif (self.method == OPTIONS[2]):
				validate_ed_dataset(self.dataset1)
				validate_ed_dataset(self.dataset2)

				dataset1_dict = self.ed_datasets[self.dataset1]
				dataset1_key = list(dataset1_dict.keys())
				dataset1_json = dataset1_dict.get(dataset1_key[0])[1]
				df1 = pd.read_json(dataset1_json)

				validate_column(df1, self.column1)
				validate_column(df1, self.column2)

				dataset2_dict = self.ed_datasets[self.dataset2]
				dataset2_key = list(dataset2_dict.keys())
				dataset2_json = dataset2_dict.get(dataset2_key[0])[1]
				df2 = pd.read_json(dataset2_json)

				validate_column(df2, self.column1)
				validate_column(df2, self.column2)
				return self.ed_component.scatter_compare(df1, df2, self.column1, self.column2)
			elif (self.method == OPTIONS[3]):
				validate_ed_dataset(self.dataset1)

				dataset1_dict = self.ed_datasets[self.dataset1]
				dataset1_key = list(dataset1_dict.keys())
				dataset1_json = dataset1_dict.get(dataset1_key[0])[1]
				df = pd.read_json(dataset1_json)

				validate_column(df, self.column1)
				return self.ed_component.statistics(df, self.column1)
			elif (self.method == OPTIONS[4]):
				validate_ed_dataset(self.dataset1)
				validate_ed_dataset(self.dataset2)

				dataset1_dict = self.ed_datasets[self.dataset1]
				dataset1_key = list(dataset1_dict.keys())
				dataset1_json = dataset1_dict.get(dataset1_key[0])[1]
				df1 = pd.read_json(dataset1_json)

				validate_column(df1, self.column1)

				dataset2_dict = self.ed_datasets[self.dataset2]
				dataset2_key = list(dataset2_dict.keys())
				dataset2_json = dataset2_dict.get(dataset2_key[0])[1]
				df2 = pd.read_json(dataset2_json)

				validate_column(df2, self.column2)
				return self.ed_component.statistics_columns(df1, df2, self.column1, self.column2)
		except Exception as e:
			error_message = '{0} Could not plot, invalid input format. Check these are correct ---> {1} {2} {3}'.format(e, self.method, self.json_indexes, self.columns)
			raise Exception(error_message)


	def validate_ed_dataset(dataset_index):
		try:
			assert(dataset_index >= 0)
			assert(len(self.ed_datasets) > dataset_index)
		except:
			raise Exception('Invalid index for dataset.')

	def validate_column(df, column):
		try:
			columns = list(df.columns.values)
			assert(columns.contains(column))
		except:
			raise Exception('Invalid column {0}'.format(column))	
