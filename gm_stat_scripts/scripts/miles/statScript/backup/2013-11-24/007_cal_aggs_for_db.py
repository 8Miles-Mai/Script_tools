#!/usr/local/bin/python





from gm_common import *


def flush_to_db():
    log("flushing to aggs table...")
    
    action_data=[]
    effect_data=[]
    total=0
    
    for key in action_aggs_counter :
        item = aggs_log()
        item_arr=[]
        item_arr=action_aggs_counter[key]
        item.ind_group_id=item_arr[0]
        item.stat_type=item_arr[1]
        item.min_count=item_arr[2]
        item.avg_count_wla=item_arr[3]
        item.avg_count_all=item_arr[4]
        item.max_count=item_arr[5]
        action_data.append(item)
        total=total+1
    
    for key in effect_aggs_counter :
        item = aggs_log()
        item_arr=[]
        item_arr=effect_aggs_counter[key]
        item.ind_group_id=item_arr[0]
        item.stat_type=item_arr[1]
        item.min_count=item_arr[2]
        item.avg_count_wla=item_arr[3]
        item.avg_count_all=item_arr[4]
        item.max_count=item_arr[5]
        effect_data.append(item)
        total=total+1
         
    year_id=get_curr_year_no()
    week_id=get_curr_week_no()
    stat_date=get_curr_date()
    log("start to load aggsregation data. year: " + str(year_id) + " week: " + str(week_id))   
    load_to_client_aggs_table(year_id=year_id,
                    week_id=week_id,
                    stat_date=stat_date,
                    action_data=action_data,
                    effect_data=effect_data)
    
    log("insert total " + str(total) + " records")            
    return True


if __name__ == "__main__":

    # restore cache data
    sdict,cdict,udict=get_supplier_list() 
    
    # calculate the number of company for each group type, for the average calculation
    group_id_counter=[0 for x in range(0,100)]
    for key in cdict:
        type=cdict[key]
        group_id_counter[type]=group_id_counter[type]+1
    
        
    # global variables 
    year_id=get_curr_year_no()
    week_id=get_curr_week_no()
    

    
    
    action_aggs_counter = {}
    effect_aggs_counter = {}

    
    #fetch max counter in each industry group from wla$client_action_daily
    msSql= """
            select sumAggs.ind_group_id,sumAggs.action_type,min(sumcount),avg(sumcount),sum(sumcount) from
            (select comp_id,ind_group_id,action_type,sum(count) as sumcount
            from wla$client_action_daily
            where year_id=%s and week_id=%s
            group by comp_id,ind_group_id,action_type) as sumAggs
            group by sumAggs.ind_group_id,sumAggs.action_type;
            """
            

    msConn=get_mysql_conn()
    msCurr=msConn.cursor()
    msCurr.execute(msSql,(year_id,week_id))
    key=0

    for msRs in msCurr.fetchall():

        group_id=msRs[0]
        action_type=msRs[1]
        min=msRs[2]      
        avg_wla=msRs[3]
        sum=msRs[4]
        avg_all=sum/group_id_counter[group_id]
        

        item_arr=[]
        item_arr.append(group_id)
        item_arr.append(action_type)
        item_arr.append(min)
        item_arr.append(avg_wla)
        item_arr.append(avg_all)
        
        subMsCurr=msConn.cursor()
        subMsSql= """
                select comp_id,sum(count) 
                from wla$client_action_daily
                where ind_group_id=%s and action_type=%s and year_id=%s and week_id=%s
                group by comp_id order by sum(count) desc limit 0,10;
                """
            
        subMsCurr.execute(subMsSql,(group_id,action_type,year_id,week_id))
        top10sum=0
        top10count=0
        for subMsRs in subMsCurr.fetchall():
            top10count=top10count+1
            top10sum=top10sum+subMsRs[1]
        
        
        
        top10avg=top10sum/top10count
        
        item_arr.append(top10avg)
        
        action_aggs_counter[key]=item_arr
        key=key+1        
    
    

    
    
    #fetch max counter in each industry group from wla$client_effect_daily    
    msSql= """
            select sumAggs.ind_group_id,sumAggs.stat_type,min(sumcount),avg(sumcount),sum(sumcount) from
            (select comp_id,ind_group_id,stat_type,sum(count) as sumcount
            from wla$client_effect_daily
            where year_id=%s and week_id=%s
            group by comp_id,ind_group_id,stat_type) as sumAggs
            group by sumAggs.ind_group_id,sumAggs.stat_type;
            """
            

    key=0

    msCurr.execute(msSql,(year_id,week_id))

    for msRs in msCurr.fetchall():

        group_id=msRs[0]
        stat_type=msRs[1]
        min=msRs[2]
        avg_wla=msRs[3]
        sum=msRs[4]
        avg_all=sum/group_id_counter[group_id]

        item_arr=[]
        item_arr.append(group_id)
        item_arr.append(stat_type)
        item_arr.append(min)
        item_arr.append(avg_wla)
        item_arr.append(avg_all)
        
        subMsCurr=msConn.cursor()
        subMsSql= """
                  select comp_id,sum(count) 
                  from wla$client_effect_daily
                  where ind_group_id=%s and stat_type=%s and year_id=%s and week_id=%s
                  group by comp_id order by sum(count) desc limit 0,10;
                  """
            
        subMsCurr.execute(subMsSql,(group_id,stat_type,year_id,week_id))
        top10sum=0
        top10count=0
        for subMsRs in subMsCurr.fetchall():
            top10count=top10count+1
            top10sum=top10sum+subMsRs[1]
        
        
        
        top10avg=top10sum/top10count
        
        item_arr.append(top10avg)

        effect_aggs_counter[key]=item_arr
        key=key + 1
                

                
    msConn.close()
    
    
    


    # At the end flush to db 
    flush_to_db()
