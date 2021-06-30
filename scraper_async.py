# import requests
import wikitextparser as wtp
import json
import re
# import pandas as pd
import os
import os.path
import asyncio
from functools import wraps
import httpx
from timeit import default_timer as timer
from wikitextparser import remove_markup, parse
from collections import Counter, OrderedDict


new_keys_dict={}
new_keys_list=[]


all_substances=[]



# loop = asyncio.get_event_loop()
start = timer()


# def request_concurrency_limit_decorator(limit=3):
#     # Bind the default event loop 
#     sem = asyncio.Semaphore(limit)

#     def executor(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             async with sem:
#                 return await func(*args, **kwargs)

#         return wrapper

#     return executor








def replace_all(text, replace_dict):
    for i, j in replace_dict.items():
        text = text.replace(i, j)
    return text


def parse_wiki_template(t): 
    # print(t.pformat())
    result_dict={}
    for item in t.arguments:
        item_name=item.name.strip()
        item_value=item.value.strip()

        


        ignored_items=[
            'Verifiedfields',
            'Watchedfields',
            'verifiedrevid',
            'ImageFile',
            'ImageFileL1',
            'ImageFileL1_Ref',
            'ImageNameL1',
            'ImageFileR1',
            'ImageFileR1_Ref',
            'ImageNameR1',
            'ImageFile2',
            'ImageFile2_Ref',
            'ImageSize2',
            'ImageName2',
            'CASNo_Ref',
            'ChemSpiderID_Ref',
            'UNII_Ref',
            'DrugBank_Ref',
            'KEGG_Ref',
            'ChEBI_Ref',
            'ChEMBL_Ref',
            'StdInChI_Ref',
            'StdInChIKey_Ref',
            'ImageFile1',
            'ImageSize1',
            'ImageName1',
            'ImageName',
            'ImageSize',
            'ImageAlt',
            'ImageAlt1',
            'Reference',
            'ImageFileL2',
            'ImageNameL2',
            'ImageFileR2',
            'ImageNameR2',
            'ImageSizeL1',
            'ImageSizeR1',
            'ImageAltL1',
            'ImageAltR1',
            'ImageAltL2',
            'ImageAltR2',
            'ImageFile3',
            'ImageSize3',
            'ImageName3',
            'ImageSizeL2',
            'ImageSizeR2',
            'Verifiedimages',
            'ImageCaption',
            'ImageCaption3',
            'ImageCaptionL1',
            'ImageCaptionR1',
            'ImageCaptionL2',
            'ImageCaptionR2',
            'ImageFileL3',
            'ImageSizeL3',
            'ImageCaptionL3',
            'ImageFileR3',
            'ImageSizeR3',
            'ImageCaptionR3',
        ]
        standard_items=[
            'Name',
            'PIN',
            'CASNo',
            'PubChem',
            'ChemSpiderID',
            'UNII',
            'EINECS',
            'UNNumber',
            'DrugBank',
            'KEGG',
            'MeSHName',
            'ChEBI',
            'ChEMBL',
            'RTECS',
            'Beilstein',
            'Gmelin',
            '3DMet',
            'SMILES',
            'StdInChI',
            'InChI',
            'StdInChIKey',
            'C',
            'H',
            'O',
            'Cl',
            'N',
            'Appearance',
            'Odor',
            'Density',
            'MeltingPtC',
            'BoilingPtC',
            'Solubility',
            'SolubleOther',
            'LogP',
            'RefractIndex',
            'Viscosity',
            'Dipole',
            'pKa',
            'VaporPressure',
            'MagSus',
            'DeltaHf',
            'DeltaHc',
            'Entropy',
            'ExternalSDS',  ##
            'NFPA-H',
            'NFPA-F',
            'NFPA-R',
            'FlashPtC',
            'AutoignitionPtC',
            'ExploLimits',
            'LD50',
            'PEL',
            'IDLH',
            'REL',
            'LC50',  ##
            'LDLo',  ##
            'LCLo',  ##
            'MeltingPtK',
            'BoilingPtK',
            'HeatCapacity',
            'GHSSignalWord', ##
            'data page pagename',
            'pKb',
            'ATCCode_prefix',
            'ATCCode_suffix',
            'InChIKey',
            'NFPA-S',
            'EC_number',
            'FlashPt',
            'CASNo1',
            'CASNo2',
            'CASNo1_Comment',
            'CASNo2_Comment',
            'UNII1_Comment',
            'UNII2_Comment',
            'PubChem1_Comment',
            'PubChem2_Comment',
            'UNII1',
            'UNII2',
            'PubChem1',
            'PubChem2',
            'ChemSpiderID1',
            'ChemSpiderID1_Comment',
            'ChemSpiderID2',
            'ChemSpiderID2_Comment',
            'OtherFunction_label', # multiple ?
            'Formula',
            'MolarMass',
            'HenryConstant',
            'SystematicName',
            'SMILES_Comment',
            'InChI1',
            'InChIKey1',
            'SMILES1',
            'SMILES1_Comment',
            'Solvent',
            'BoilingPt_notes',
            'LambdaMax',
            'MolShape',
            'CrystalStruct',
            'MainHazards',
            'OtherAnions',
            'OtherCations',
            'DTXSID',
            'Absorbance',
            'TLV-TWA',
            'IUPHAR_ligand',
            'Odour',
            'FlashPtK',
            'AutoignitionPtK',
            'Legal_AU',
            'Legal_CA',
            'BoilingPt',
            'SublimationConditions',
            'MeltingPt_notes',
            'ConjugateAcid',
            'IUPACName',
            'MolarMassUnit',
            'FlashPtF',
            'ConjugateBase',
            'CASNo_Comment',
            'Coordination',  ## <br />
            'SpaceGroup',
            'LattConst_a',
            'LattConst_b',
            'LattConst_c',
            'UnitCellFormulas',
            'DeltaGf',
            'Solvent1',
            'Solvent2',
            'Solvent3',
            'Solubility1',
            'Solubility2',
            'Solubility3',
            'MeltingPt',
            'PointGroup',
            'ThermalConductivity',
            

        ]

        section_items=[
            'Section1',
            'Section2',
            'Section3',
            'Section4',
            'Section5',
            'Section6',
            'Section7',
            'Section8',
        ]

        if item_value=="<small>(''S'')</small>":
            item_value='S'
        if item_value=="<small>(''R'')</small>":
            item_value='R'





        if item_value == '': 
            pass
        
        elif item_name[-4:].lower() in '_ref': 
            pass
        

        elif item_name in ignored_items: 
            pass


        elif item_name in standard_items:
            replace_dict={
                '<sup>':'^',
                '</sup>':'',
                '&nbsp;':' ',
                '[':'',
                ']':'',
                '<sub>':'',
                '</sub>':'',
            }
            item_value = replace_all(item_value,replace_dict) # string cleaning
            
            item_value = re.sub('<ref.*?</ref>', '', item_value) # remove wikipedia references
            item_value = re.sub('<ref .*?/>', '', item_value) # remove wikipedia references

            result_dict.update({item_name:item_value})


        elif item_name in section_items:
            if item.templates:  # if not empty
                section_dict= parse_wiki_template(item.templates[0]) 
                # result_dict.update({item_name:section_dict})
                for section_key, section_value in section_dict.items():
                    if (section_key in result_dict) and (section_key  !='Dipole'):
                        raise('reapeated key')
                    result_dict.update({section_key:section_value})


        elif item_name in ['OtherNames','OtherCompounds','OtherFunction']: 
            replace_dict={
                '<sup>':'^',
                '</sup>':'',
                '&nbsp;':' ',
                '<sub>':'',
                '</sub>':'',
                '<br/>':'<br />',
                '<br>':'<br />',
                "'":"",
                '[':'',
                ']':'',
            }
            item_value = replace_all(item_value,replace_dict)
            
            item_values = item_value.split("<br />")

            result_dict.update({item_name:item_values})


        elif item_name in ['GHSPictograms']: 
            item_value= item_value.removeprefix('{{')
            item_value= item_value.removesuffix('}}')
            
            item_values = item_value.split("}}{{")

            result_dict.update({item_name:item_values}) 
               
        elif item_name in ['HPhrases']: 
            item_value= item_value.removeprefix('{{H-phrases|')
            item_value= item_value.removesuffix('}}')
            item_values = item_value.split("|")

            item_values= ['H' + item_value for item_value in item_values] # add prefix

            result_dict.update({item_name:item_values})    

        elif item_name in ['PPhrases']: 
            item_value= item_value.removeprefix('{{P-phrases|')
            item_value= item_value.removesuffix('}}')
            item_values = item_value.split("|")

            item_values= ['P' + item_value for item_value in item_values] # add prefix

            result_dict.update({item_name:item_values})    

        else:
            # print(f'Not supported item:  {item_name}    {item_value}')
            new_keys_dict.update({item_name:item_value})
            new_keys_list.append(item_name)
            with open(f'./not_supported.txt', 'a') as the_file:
                the_file.write(f'Not supported item:\t{item_name} \t{item_value}\r\n')
    return result_dict




# @request_concurrency_limit_decorator(limit=3)
async def scrap_substance(substance):


    if os.path.isfile(f'./substances/{substance}.txt') :
        return

    if not substance:
        return


    end = timer()
    print(f'time5: {end - start}')

    wikipedia_title=substance[:]

    url=f'https://en.wikipedia.org/w/index.php?title={wikipedia_title}&action=raw'
    # response = requests.get(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)

    end = timer()
    print(f'time6: {end - start}')

    if response.status_code== 404:
        print(f'404: {substance}')
        with open(f'./substances/{substance}.txt', 'w') as the_file:
            the_file.write('404')  
        return

    if response.text[:9].upper()=='#REDIRECT':
        wikipedia_title = re.search('\[\[(.+?)\]\]', response.text.split('\n')[0]).group(1).strip() # new title after redirect
        print(f'redirect: {substance} -> {wikipedia_title}')
        
        url=f'https://en.wikipedia.org/w/index.php?title={wikipedia_title}&action=raw'
        # response = requests.get(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)

    # with open(f'./substances/{substance}_wikitext.txt', 'w') as the_file:
    #     the_file.write(response.text)

    # text= response.text ##

    parsed = wtp.parse(response.text)

    print(substance)
    print()

    chembox=False
    for t in parsed.templates:
        if t.name.strip().lower() in ['chembox','chembox\n<!-- images -->', 'chembox <!-- infobox -->']:
            chembox=True
            result_dict = parse_wiki_template(t)
            print()

            with open(f'./substances/{substance}.txt', 'w') as the_file:
                the_file.write(json.dumps(result_dict))

            all_substances.append(result_dict)

            break
    if not chembox:
        print(f'No chembox: {substance} $$ {wikipedia_title}')      






async def main():

    if not os.path.isdir('./substances/'):
        os.mkdir('./substances/')




    end = timer()
    print(f'time2: {end - start}')

    print('start')


    with open('substances_list_modified.txt') as f:
        substances =f.read().splitlines()

    end = timer()
    print(f'time3: {end - start}')

    tasks=[]

    for substance in substances:


        tasks.append(scrap_substance(substance))
        # tasks.append(asyncio.create_task())

    end = timer()
    print(f'time4: {end - start}')

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(tasks))
    await asyncio.gather(*tasks)

    # asyncio.run_until_complete(asyncio.wait(tasks))

    # with open('new_keys_dict.txt', 'a') as the_file:
    #     for i, j in new_keys_dict.items():
    #         the_file.write(f'{i}   {j}' +'\n')

    # with open('new_keys_dict2.txt', 'a') as the_file:
    #     for i, j in new_keys_dict.items():
    #         the_file.write(f'{i}' +'\n')

    # counter =Counter(new_keys_list)

    # with open('new_keys_dict3.txt', 'a') as the_file:
    #     for i, j in counter.items():
    #         the_file.write(f'{i}   {j}' +'\n')
    
    # with open('new_keys_dict4.txt', 'a') as the_file:
    #     for i, j in OrderedDict(counter.most_common()).items():
    #         the_file.write(f'{i}   {j}' +'\n')
    
    with open('all_substances.json', 'w') as the_file:
            the_file.write(json.dumps(all_substances))


    





if __name__ == '__main__':
    
    end = timer()
    print(f'time1: {end - start}')


    asyncio.run(main())
    

    # df = pd.read_excel('substances_scraping_wikipedia_info.xlsx') # can also index sheet by name or fetch all sheets
    # substances = df['substances'].tolist()









    # loop.close()
















     ### TODO remove_markup
                
    #### TODO: dodać usuwanie linków            
    #### TODO: przeszukać small           