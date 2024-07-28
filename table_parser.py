files = [(2005,'cancer-facts-and-figures-2005_table1.txt'),
(2006,'cancer-facts-and-figures-2006_table1.txt'),
(2007,'cancer-facts-and-figures-2007_table1.txt'),
(2008,'cancer-facts-and-figures-2008_table1.txt'),
(2009,'cancer-facts-and-figures-2009_table1.txt'),
(2010,'cancer-facts-and-figures-2010_table1.txt'),
(2011,'cancer-facts-and-figures-2011_table1.txt'),
(2012,'cancer-facts-and-figures-2012_table1.txt'),
(2013,'cancer-facts-and-figures-2013_table1.txt'),
(2014,'cancer-facts-and-figures-2014_table1.txt'),
(2015,'cancer-facts-and-figures-2015_table1.txt'),
(2016,'cancer-facts-and-figures-2016_table1.txt'),
(2017,'cancer-facts-and-figures-2017_table1.txt'),
(2018,'cancer-facts-and-figures-2018_table1.txt'),
(2019,'cancer-facts-and-figures-2019_table1.txt'),
(2020,'cancer-facts-and-figures-2020_table1.txt'),
(2021,'cancer-facts-and-figures-2021_table1.txt'),
(2022,'cancer-facts-and-figures-2022_table1.txt'),
(2023,'cancer-facts-and-figures-2023_table1.txt'),
(2024,'cancer-facts-and-figures-2024_table1.txt')]

#types = ['All sites','All Sites','Oral cavity & pharynx','Digestive system','Respiratory system','Bones & joints','Soft tissue',
#'Skin','Breast','Genital system','Urinary system','Eye & orbit','Brain & other nervous system',
#'Endocrine system','Lymphoma','Myeloma','Leukemia','Other & unspecified']

types = ['All sites', 'Oral cavity & pharynx','Digestive system','Respiratory system','Bones & joints','Soft tissue',
'Skin','Breast','Genital system','Urinary system','Eye & orbit','Brain & other nervous system',
'Endocrine system','Lymphoma','Myeloma','Leukemia']

scatter_dict = dict()
for type_title in types :
    scatter_dict[type_title] = [0,0,0,0,0,0]
    with open('data_details_' + type_title + '.csv', 'w') as details_file:
        header = ['year','CasesBoth','CasesMale','CasesFemale','DeathsBoth','DeathsMale','DeathsFemale']
        details_file.write(','.join(header)+'\n')

for file_tuples in files :
    year = file_tuples[0]
    print("file name:", file_tuples[1], "year", year)
    
    with open(file_tuples[1], 'r') as data_file:
        with open('data_scatter_' + str(year) + '.csv', 'w') as year_scatter_file:
            header = ['type','CasesBoth','CasesMale','CasesFemale','DeathsBoth','DeathsMale','DeathsFemale']
            year_scatter_file.write(','.join(header)+'\n')
            data_lines = data_file.readlines()
            for line in data_lines[3:] :
                # clean up title changes between data years
                line = line.replace('All Sites','All sites')
                line = line.replace('Multiple myeloma','Myeloma')
                for type_title in types :
                    with open('data_details_' + type_title + '.csv', 'a') as details_file:
                        if (type_title in line) :
                            line = line.replace(',', '')
                            split_line = line.split()
                            data_row = split_line[-6:]
                            for i in range(6) :
                                scatter_dict[type_title][i] += int(data_row[i])
                            if (type_title != 'All sites') :
                                year_scatter_file.write(type_title + ',' + ','.join(data_row)+'\n')
                            details_file.write(str(year) + ',' + ','.join(data_row)+'\n')

with open('data_scatter.csv', 'w') as scatter_file:
    header = ['type','CasesBoth','CasesMale','CasesFemale','DeathsBoth','DeathsMale','DeathsFemale']
    scatter_file.write(','.join(header)+'\n')
    for (key, item) in scatter_dict.items() :
        scatter_file.write(key + ',' + ','.join(map(str, item))+'\n')
            