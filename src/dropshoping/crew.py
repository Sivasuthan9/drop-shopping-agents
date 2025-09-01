from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.data_tools import (
    ReadCSVTool, WriteJSONTool, WriteCSVTool, 
    CalculatePricingTool, FilterProductsTool
)
from .tools.file_tools import WriteFileTool, ReadFileTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class Dropshoping():
    """Dropshoping crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'],
            verbose=True,
            tools=[ReadFileTool(), WriteFileTool()],
            allow_delegation=True
        )

    @agent
    def product_sourcing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['product_sourcing_agent'],
            verbose=True,
            tools=[ReadCSVTool(), FilterProductsTool(), WriteJSONTool()]
        )

    @agent
    def listing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['listing_agent'],
            verbose=True,
            tools=[ReadFileTool(), WriteJSONTool()]
        )

    @agent
    def pricing_stock_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pricing_stock_agent'],
            verbose=True,
            tools=[ReadFileTool(), CalculatePricingTool(), WriteCSVTool()]
        )

    @agent
    def order_routing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['order_routing_agent'],
            verbose=True,
            tools=[ReadCSVTool(), ReadFileTool(), WriteJSONTool()]
        )

    @agent
    def qa_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_agent'],
            verbose=True,
            tools=[ReadFileTool(), WriteJSONTool()]
        )

    @agent
    def reporter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter_agent'],
            verbose=True,
            tools=[ReadFileTool(), WriteFileTool()]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def workflow_coordination_task(self) -> Task:
        return Task(
            config=self.tasks_config['workflow_coordination_task'],
            agent=self.manager_agent()
        )

    @task
    def product_sourcing_task(self) -> Task:
        return Task(
            config=self.tasks_config['product_sourcing_task'],
            agent=self.product_sourcing_agent()
        )

    @task
    def listing_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['listing_generation_task'],
            agent=self.listing_agent()
        )

    @task
    def pricing_stock_task(self) -> Task:
        return Task(
            config=self.tasks_config['pricing_stock_task'],
            agent=self.pricing_stock_agent()
        )

    @task
    def order_routing_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_routing_task'],
            agent=self.order_routing_agent()
        )

    @task
    def qa_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['qa_review_task'],
            agent=self.qa_agent()
        )

    @task
    def daily_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['daily_report_task'],
            agent=self.reporter_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Dropshoping crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
