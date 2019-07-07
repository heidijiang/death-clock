import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
import calendar
import argparse


COLOR = 'w'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
mpl.rcParams['font.family'] = "Andale Mono"

def process_table(infile,outfile):
    df = pd.read_csv(infile)
    for c in ['num_m','num_f']:
        df[c] = df[c].str.replace(',','').astype('int64')
        
    df['all'] = (df['prob_m']*df['num_m'] + df['prob_f']*df['num_f'])
    df['pdf'] = df['all']/df['all'].sum()
    df = df[df['all']>0]
    df.to_csv(outfile)

class Deathday():
    
    def __init__(self,name,age=None):
        
        self.name = name

        try:
            self.age = self.check_age(int(age))
        except:
            print('Age is invalid! Using default age!')
            self.age = self.default_age()

        self.dob = self.get_dob()
        self.df_w_age = self.adjust_dist()
        self.death_age = self.age_of_death()
        self.death_date = self.get_death_date()
        

    def get_dob(self):
        dt = self.today()
        return datetime.date(dt.year-self.age,dt.month,dt.day)
    
    def default_age(self):
        return 38

    def check_age(self,age):
            
        if age >= df['age'].max() or age <= 0:
            print('Age is invalid! Using default age!')
            age = self.default_age()
        
        return age
        
    def today(self):
        return datetime.date.today()
    
    def adjust_dist(self):
        
        df_w_age = df[df['age']>self.age].copy().reset_index()
        df_w_age['pdf'] = df_w_age['all']/df_w_age['all'].sum()
        df_w_age['cdf'] = df_w_age['pdf'].cumsum()

        yr_diff = df_w_age['age'].max()-df_w_age['age'].min()+1
        df_w_age['year'] = np.arange(self.today().year,self.today().year+yr_diff)
        return df_w_age
    

    def age_of_death(self):
        r = np.random.random(1)[0]
        idx = (self.df_w_age['cdf']-r).abs().idxmin()
        if r>=self.df_w_age['cdf'].iloc[idx]:
            idx+=1
        death_age = self.df_w_age['age'].iloc[idx]
        return death_age

    def random_date(self,year):
        if year == self.today().year:
            start_date = self.today().toordinal()
        else:
            start_date = datetime.date(year,1,1).toordinal()
        end_date = datetime.date(year,12,31).toordinal()
        return datetime.date.fromordinal(np.random.randint(start_date, end_date))

    def get_death_date(self):
        death_year = self.dob.year + self.death_age
        return self.random_date(death_year)
    

    def printed_date(self):
        months = [i for i in calendar.month_abbr]
        dt = self.death_date
        return '{} {}, {}'.format(months[dt.month],dt.day,dt.year)

    
    def __repr__(self):
        return '{}, you will die on: {}'.format(self.name,self.death_date)

    
    def __str__(self):
        self.display()
        return '\n\n\t\t\t{}, you will die on: {}'.format(self.name,self.printed_date())
    

    def display(self):
        fig,ax = plt.subplots(1,2,figsize=(10,4))
        sns.lineplot(data=self.df_w_age,x='year',y='pdf',ax=ax[0], color='pink')
        ax[0].scatter(self.death_date.year,self.df_w_age.loc[self.df_w_age['year']==self.death_date.year,'pdf'],c='red')
        ax[0].set_ylabel('Probability of death')
        sns.lineplot(data=self.df_w_age,x='year',y='cdf',ax=ax[1], color='pink')
        ax[1].scatter(self.death_date.year,self.df_w_age.loc[self.df_w_age['year']==self.death_date.year,'cdf'],c='red')
        ax[1].set_ylabel('Cumulative probability of death')
        c = 'w'
        for a in ax:
            a.spines['bottom'].set_color(c)
            a.spines['top'].set_color(c)
            a.spines['left'].set_color(c)
            a.spines['right'].set_color(c)
        plt.show()

def get_df():
    global df
    df = pd.read_csv('life_table_2015_processed.csv')

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, nargs='+', default='Ben')
    
    parser.add_argument('--age', type=str,
                        default=38)
    args = parser.parse_args()
    get_df()

    out = Deathday(args.name,args.age)
    out.display()
    with open('tmp.txt', 'w') as f:
        f.write(out.printed_date()+'\n')
        f.write(str(out.death_age))



if __name__ == '__main__':
    main()


