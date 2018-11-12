# coding: utf-8

import pandas as pd
import pprint
import os
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

def open_table_list_columns(DATADIR, table, compression=None):
    if compression is None:
        table = pd.read_csv(os.path.join(DATADIR, table+'.csv'), dtype=object, compression=compression)
    else:
        table = pd.read_csv(os.path.join(DATADIR, table + '.csv.gz'), dtype=object, compression=compression)
    pp = pprint.PrettyPrinter()
    pp.pprint(list(table.columns))
    return table

def groupby_percent(df, groupby_var, unit_var, figsize=(10, 5)):
    x = df.groupby(groupby_var).count().reset_index()
    x['percent'] = 100*x[unit_var]/x[unit_var].sum()
    x = x.sort_values(['percent'])

    s = pd.DataFrame(x[[groupby_var, unit_var,'percent']])

    return(s, x.plot(x=groupby_var, y='percent', kind='barh', figsize=figsize, color='#2B8CC4'))


def groupby_plotsize(df, groupby_var, figsize=(10, 5)):
    return(df.groupby(groupby_var).size().sort_values(ascending=True).plot(kind = 'barh',
                                                                           figsize=figsize,
                                                                           color='#2B8CC4'
                                                                           )
           )


def plot_time_metric_byvar(df, metric, byvar):
    grouped = df.groupby([byvar, pd.Grouper(freq='D')])[metric].sum()
    by_day = grouped.unstack(byvar, fill_value=0)
    top = by_day.iloc[:, by_day.columns.isin(by_day.min().sort_values(ascending=False)[:10].index)]
    bottom = by_day.iloc[:, by_day.columns.isin(by_day.min().sort_values()[:10].index)]

    ax = top.plot()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel(metric)
    ax.set_xlabel('Date')
    ax.set_title('Top 10 {}s for {}'.format(byvar, metric))

    ay = bottom.plot()
    ay.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ay.set_ylabel(metric)
    ay.set_xlabel('Date')
    ay.set_title('Bottom 10 {}s for {}'.format(byvar, metric))

    return ax, ay


def create_collapsed_dreason(df, discharge_codes):
    df['df_reason'] = df['NDTMSReasonForClosure'].map(discharge_codes).astype('category')
    df['collapsed_dreason'] = df['df_reason'].cat.add_categories(["treatment completed - drug free",
                                                                                  'transferred',
                                                                                  'moved',
                                                                                  'dropped out/unable to engage',
                                                                                  'treatment completed - onward referral',
                                                                                  'treatment unknown/withdrawn/innappropriate - onward referral',
                                                                                  'treatment completed - occasional use (not crack/heroin)',
                                                                                  'treatment unknown/withdrawn/innappropriate',
                                                                                  'unknown/other',
                                                                                  'died'])

    df.loc[(df['df_reason'] == 'Treatment completed drug free') |
              (df['df_reason'] == 'Treatment completed drug-free')|
              (df['df_reason'] == 'Comp drug free no agreed lead agency')|
              (df['df_reason'] == 'Comp drug free ref child looked after service')|
              (df['df_reason'] == 'Comp drug free ref criminal justice service')|
              (df['df_reason'] == 'Comp drug free ref health or mental health service')|
              (df['df_reason'] == 'Comp drug free ref other adult service')|
              (df['df_reason'] == 'Comp drug free ref targeted youth support service')|
              (df['df_reason'] == 'DIP only - Care plan/treatment complete // Treatment completed')|
              (df['df_reason'] == 'PbR only - Treatment completed drug free'),
              'collapsed_dreason'] = 'treatment completed - drug free'

    df.loc[(df['df_reason'] == 'Treatment completed occasional user (not heroin or crack)') |
              (df['df_reason'] == 'PbR only - Treatment Completed Occasional User (not heroin or crack)'),
           'collapsed_dreason'] = 'treatment completed - occasional use (not crack/heroin)'

    df.loc[(df['df_reason'] == 'Treatment completed drug free') |
              (df['df_reason'] == 'Transferred not in custody')|
              (df['df_reason'] == 'Transferred in custody')|
              (df['df_reason'] == 'Transferred – Transition to adult substance misuse service')|
              (df['df_reason'] == 'Transferred – programme completed at the residential provider – additional community treatment required')|
              (df['df_reason'] == 'Transferred – programme completed at the residential provider – additional residential treatment required')|
              (df['df_reason'] == 'Transferred – programme not completed at the residential provider – additional community treatment required')|
              (df['df_reason'] == 'DIP only - Client transferred to another DAT give DAT code // Moved away')|
              (df['df_reason'] == 'DIP only - Client begun a community sentence (eg DTTO,DRR) and is no longer case managed by the CJIT // Referred on')|
              (df['df_reason'] == 'Retained in custody')|
              (df['df_reason'] == 'DIP only - Client transferred to prison give prison code // Prison')|
              (df['df_reason'] == 'Incomplete retained in custody')|
              (df['df_reason'] == 'Transferred – programme not completed at the residential provider – additional residential treatment required'),
           'collapsed_dreason'] = 'transferred'

    df.loc[(df['df_reason'] == 'Moved no agreed lead agency') |
              (df['df_reason'] == 'Moved ref child looked after service')|
              (df['df_reason'] == 'Moved ref criminal justice service')|
              (df['df_reason'] == 'Moved ref health or mental health service')|
              (df['df_reason'] == 'Moved ref targeted youth support service'),
           'collapsed_dreason'] = 'moved'

    df.loc[(df['df_reason'] == 'Dropped out no agreed lead agency') |
              (df['df_reason'] == 'Dropped out ref adult treatment provider')|
              (df['df_reason'] == 'Dropped out ref child looked after service')|
              (df['df_reason'] == 'Dropped out ref criminal justice service')|
              (df['df_reason'] == 'Dropped out ref health or mental health service')|
              (df['df_reason'] == 'Dropped out ref targeted youth support service')|
              (df['df_reason'] == 'DIP only - Client disengaged // Dropped out/left')|
              (df['df_reason'] == 'Client unable to engage')|
              (df['df_reason'] == 'Incomplete treatment commencement declined by client')|
              (df['df_reason'] == 'Treatment declined by client')|
              (df['df_reason'] == 'Dropped out ref other adult service'),
              'collapsed_dreason'] = 'dropped out/unable to engage'

    df.loc[(df['df_reason'] == 'Comp ref adult treatment provider') |
              (df['df_reason'] == 'Comp ref child looked after service')|
              (df['df_reason'] == 'Comp ref criminal justice service')|
              (df['df_reason'] == 'Comp ref health or mental health service')|
              (df['df_reason'] == 'Comp ref targeted youth support service')|
              (df['df_reason'] == 'Comp ref other adult service'),
              'collapsed_dreason'] = 'treatment completed - onward referral'

    df.loc[(df['df_reason'] == 'Other ref criminal justice service')|
              (df['df_reason'] == 'Other ref targeted youth support service')|
              (df['df_reason'] == 'Withdrawn ref targeted youth support service')|
              (df['df_reason'] == 'Approp treat na no agreed lead agency')|
              (df['df_reason'] == 'Approp treat na ref adult treatment provider')|
              (df['df_reason'] == 'Approp treat na ref child looked after service')|
              (df['df_reason'] == 'Approp treat na ref criminal justice service')|
              (df['df_reason'] == 'Approp treat na ref health or mental health service')|
              (df['df_reason'] == 'Approp treat na ref other adult service')|
              (df['df_reason'] == 'Approp treat na ref targeted youth support service')|
              (df['df_reason'] == 'Withdrawn ref criminal justice service')|
              (df['df_reason'] == 'Other ref child looked after service')|
              (df['df_reason'] == 'Other ref health or mental health service')|
              (df['df_reason'] == 'N/K ref targeted youth support service'),
              'collapsed_dreason'] = 'treatment unknown/withdrawn/innappropriate - onward referral'

    df.loc[(df['df_reason'] == 'No appropriate treatment available')|
              (df['df_reason'] == 'Treatment withdrawn/breach of contract')|
              (df['df_reason'] == 'Incomplete treatment withdrawn by provider')|
              (df['df_reason'] == 'Inappropriate referral'),
              'collapsed_dreason'] = 'treatment unknown/withdrawn/innappropriate'

    df.loc[(df['df_reason'] == 'N/K no agreed lead agency')|
              (df['df_reason'] == 'Not known')|
              (df['df_reason'] == 'Other')|
              (df['df_reason'] == ''),
              'collapsed_dreason'] = 'unknown/other'

    df.loc[(df['df_reason'] == 'DIP only - Client died // Died')|
              (df['df_reason'] == 'Incomplete client died'),
              'collapsed_dreason'] = 'died'

    df['collapsed_dreason'] = df['collapsed_dreason'].cat.remove_unused_categories()

    return df

def create_serial_epi(df):
    df['serial_epi'] = df.Serial + '_' + df.Episode
    return df

def derive_episode_vars(df):
    print("converting startdate to datetime (takes a while)")
    df['start_date'] = pd.to_datetime(df.StartDate)
    print("converting enddate to datetime (takes a while)")
    df['end_date'] = pd.to_datetime(df.EndDate)
    df = df.drop(['StartDate', 'EndDate'], axis=1).copy()
    df['episode_duration'] = df.end_date - df.start_date
    return df

def create_code_outcome():
    code = (
        "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "93", "94", "95", "96", "97", "1", "2", "3", "4",
        "5",
        "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24",
        "25",
        "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43",
        "44",
        "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62",
        "63",
        "64", "65", "66", "67", "68", "69", "70", "90", "91", "85", "88", "82", "85", "80", "84", "85", "83", "89",
        "13",
        "86", "87", "610", "600", "601", "602", "604", "605", "606", "611", "612", "613", "614", "615", "616", "617",
        "618",
        "619", "603", "607", "608", "609", "622", "620", "621", "623", "624", "625", "98", "99")
    outcome = (
        "S", "S", "S", "N", "N", "U", "U", "N", "U", "U", "N", "N", "N", "N", "N", "S", "S", "U", "U", "N", "U", "N",
        "N",
        "U", "U", "U", "U", "U", "N", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "U", "U",
        "U",
        "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "N", "N", "N", "N",
        "N",
        "N", "N", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "S", "S", "U", "U", "S", "U",
        "S",
        "N", "U", "N", "U", "U", "U", "N", "S", "N", "U", "N", "N", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U",
        "U",
        "U", "U", "N", "S", "U", "U", "U", "U", "U", "N", "U")

    code_outcomes = dict(zip(code, outcome))
    return code_outcomes

def derive_discharge_vars(df, DATADIR):

    discharge_codes_df = pd.read_csv(os.path.join(DATADIR, 'discharge_codes.csv'), dtype=object)
    discharge_codes = pd.Series(discharge_codes_df.Text.values, index=discharge_codes_df.Code).to_dict()

    df['discharge_reason'] = df['NDTMSReasonForClosure'].map(discharge_codes).astype('category')
    df = create_collapsed_dreason(df, discharge_codes).copy()

    code_outcomes = create_code_outcome()
    df['outcome'] = df['NDTMSReasonForClosure'].map(code_outcomes).astype('category')
    return df


def km_byvar(df, byvar, T, E, xlim=(0, 2000)):
    kmf = KaplanMeierFitter()
    ax = plt.subplot(111)

    indicator = (df[byvar] == "1")
    kmf.fit(T[indicator], event_observed=E[indicator], label=byvar)
    kmf.plot(ax=ax, ci_force_lines=True)
    print("Median episode duration if {} : {}".format(byvar, kmf.median_))

    kmf.fit(T[~indicator], event_observed=E[~indicator], label="not "+byvar)
    kmf.plot(ax=ax, ci_force_lines=True)
    print("Median episode duration if not {} : {}".format(byvar, kmf.median_))
    plt.xlim(xlim)
    plt.ylim(0, 1);
    plt.title("Episode lengths by {} status".format(byvar))

