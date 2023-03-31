import math

def page_total_cell(count_query,limite):
    return math.ceil(count_query/limite)
   
def page_offset(page,limite):
    return (page-1)*limite