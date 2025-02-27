from flask import Response
from flask_admin import BaseView, expose
from matplotlib import ticker

from app.models import Employee
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import io


class PlotView(BaseView):
    @expose('/')
    def index(self):
        return self.render('chief_plots.html')

    @expose('/plot')
    def country_hours(self):
        employees = Employee.query.with_entities(Employee.country, Employee.hours_month)
        df = pd.DataFrame(employees, columns=['country', 'hours_month'])

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x='country', y='hours_month', hue='country', palette='pastel', ax=ax, legend=False)

        ax.yaxis.set_major_locator(ticker.MultipleLocator(25))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))

        plt.xticks(rotation=45)
        ax.set_title('Working Hours per Month by Country')

        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        plt.close(fig)  # Free memory
        img.seek(0)

        return Response(img.getvalue(), mimetype='image/png')

    @expose('/plot2')
    def country_office_visits(self):
        employees = Employee.query.with_entities(Employee.country, Employee.office_visits)
        df = pd.DataFrame(employees, columns=['country', 'office_visits'])

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x='country', y='office_visits', hue='country', palette='pastel', ax=ax, legend=False)

        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

        plt.xticks(rotation=45)
        ax.set_title('Office visits per country')

        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        plt.close(fig)
        img.seek(0)

        return Response(img.getvalue(), mimetype='image/png')

    @expose('/plot3')
    def visits_per_office(self):
        employees = Employee.query.with_entities(Employee.office, Employee.office_visits)
        df = pd.DataFrame(employees, columns=['office', 'office_visits'])

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(df, x='office', y='office_visits', hue='office', palette='pastel', ax=ax, legend=False)

        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

        plt.xticks(rotation=45)
        ax.set_title('Office visits per office')

        img = io.BytesIO()
        fig.savefig(img, format='png', bbox_inches='tight')
        plt.close(fig)  # Free memory
        img.seek(0)

        return Response(img.getvalue(), mimetype='image/png')
