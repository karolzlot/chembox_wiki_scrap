import wikitextparser as wtp
import json
import re
import os
import os.path
import asyncio
import httpx
from wikitextparser import remove_markup
from collections import Counter, OrderedDict
from dicttoxml import dicttoxml
import urllib.parse
import aiofiles



all_substances={}


def replace_all(text, replace_dict):
    for i, j in replace_dict.items():
        text = text.replace(i, j)
    return text


def clean_value(value):
    replace_dict={
    '<sup>':'^',
    '</sup>':'',
    # '&nbsp;':' ',
    '<sub>':'',
    '</sub>':'',
    "'":"",
    }

    value = replace_all(value,replace_dict)
    value = remove_markup(value)
    return value.replace('{{','').replace('}}','').strip()



def parse_wiki_template(t): 

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
            'ImageCaption1',
            'ImageAlt2',
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
            'ExternalSDS',
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
            'LC50',
            'LDLo',
            'LCLo',
            'MeltingPtK',
            'BoilingPtK',
            'HeatCapacity',
            'GHSSignalWord',
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
            'OtherFunction_label',
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
            'Coordination',
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
            'OtherNames',
            'OtherCompounds',
            'OtherFunction',
            'PPhrases',
            'HPhrases',
            'GHSPictograms',
            'RPhrases',
            'SPhrases',
            'EUClass',
            'Abbreviations',
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

            item_value = re.sub('<ref.*?</ref>', '', item_value) # remove wikipedia references type 1
            item_value = re.sub('<ref .*?/>', '', item_value)    # remove wikipedia references type 2

            item_value = clean_value(item_value)

            result_dict.update({item_name:item_value})


        elif item_name in section_items:
            if item.templates:  # if not empty
                section_dict= parse_wiki_template(item.templates[0]) 

                for section_key, section_value in section_dict.items():
                    if (section_key in result_dict) and (section_key  !='Dipole'):
                        raise('reapeated key')
                    result_dict.update({section_key:section_value})

        else:
            # print(f'Not supported item:  {item_name}    {item_value}')

            with open(f'./not_supported.txt', 'a') as the_file:
                the_file.write(f'Not supported item:\t{item_name} \t{item_value}\r\n')
    return result_dict




async def cached_download(wikipedia_title,redirect=False):  # download wikipedia pages or takes them from cache folder

    if redirect:
        ext='.re.txt'
    else:
        ext='.txt'

    if os.path.isfile(f'./cache/{wikipedia_title}.{ext}') :

        async with aiofiles.open(f'./cache/{wikipedia_title}.{ext}', "r") as f:
            wikitext = await f.read()
    else:
        print(f'downloading {wikipedia_title}')

        url=f'https://en.wikipedia.org/w/index.php?title={wikipedia_title}&action=raw'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
        response.raise_for_status()

        async with aiofiles.open(f'./cache/{wikipedia_title}.{ext}', 'w') as cache_file:
            await cache_file.write(response.text)

        wikitext=response.text
    return wikitext



async def scrap_substance(substance):

    if not substance:
        return

    wikipedia_title=substance[:]

    wikitext= await cached_download(wikipedia_title)

    
    if wikitext[:9].upper()=='#REDIRECT':
        wikipedia_title = re.search('\[\[(.+?)\]\]', wikitext.split('\n')[0]).group(1).strip() # new title after redirect
        print(f'redirect: {substance} -> {wikipedia_title}')

        wikitext= await cached_download(wikipedia_title,redirect=True)

    parsed = wtp.parse(wikitext)

    print(f'exctracting data from wiki page: {wikipedia_title}')


    chembox=False
    for t in parsed.templates:
        if t.name.strip().lower() in ['chembox','chembox\n<!-- images -->', 'chembox <!-- infobox -->']:
            chembox=True
            result_dict = parse_wiki_template(t)

            result_dict['url']='https://en.wikipedia.org/wiki/'+urllib.parse.quote_plus(wikipedia_title)

            all_substances[substance]= result_dict

            break
    if not chembox:
        print(f'No chembox: {wikipedia_title}')      


async def main():

    if not os.path.isdir('./cache/'):
        os.mkdir('./cache/')

    with open('substances_list_modified.txt') as f:    
        substances =f.read().splitlines()

    substances = [line for line in substances if line.strip() != ""]  # remove empty substance names (empty lines)

    tasks=[]

    for substance in substances:  
        tasks.append(scrap_substance(substance))

    await asyncio.gather(*tasks)    # get all substances asynchronously, results will go to `all_substances` dict

    sorted_all_substances=[]
    for substance in substances:
        sorted_all_substances.append(all_substances[substance])
        

    print("saving results as JSON file...")
    with open('all_substances.json', 'w', encoding='utf8') as json_file:
        json.dump(sorted_all_substances, json_file, ensure_ascii=False)


    print("saving results as XML file...")
    all_substances_xml = dicttoxml(sorted_all_substances, custom_root='substances', attr_type=False)
    with open('all_substances.xml', 'wb') as xml_file:
        xml_file.write(all_substances_xml)


    print("saving results as XLSX file...")
    import pandas as pd
    df = pd.DataFrame.from_dict(sorted_all_substances)
    df= df.transpose()
    df.to_excel('all_substances.xlsx')



if __name__ == '__main__':
    

    asyncio.run(main())
