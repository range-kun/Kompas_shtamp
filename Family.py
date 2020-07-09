# -*- coding: utf-8 -*-
#|Фамилия

import pythoncom
from win32com.client import Dispatch, gencache

import LDefin2D
import MiscellaneousHelpers as MH


def get_kompas_api7():
    module = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
    api = module.IApplication(
        Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(module.IKompasAPIObject.CLSID,
                                                                 pythoncom.IID_IDispatch))
    #const = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0)
    return module, api


def get_kompas_api5():
    module = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
    api = module.KompasObject(
        Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(module.KompasObject.CLSID, pythoncom.IID_IDispatch))
    const = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0)
    return module, api, const.constants

def fill_margin(margin, name,font_size):
    kompas6_api5_module,kompas_object,kompas6_constants = get_kompas_api5()
    kompas_api7_module,application=get_kompas_api7()

    MH.iKompasObject  = kompas_object
    MH.iApplication = application

    Documents = application.Documents
    kompas_document = application.ActiveDocument
    kompas_document_2d = kompas_api7_module.IKompasDocument2D(kompas_document)
    iDocument2D = kompas_object.ActiveDocument2D()

    iStamp = iDocument2D.GetStamp()
    iStamp.ksOpenStamp()
    iStamp.ksColumnNumber(margin)

    iTextLineParam = kompas6_api5_module.ksTextLineParam(kompas_object.GetParamStruct(kompas6_constants.ko_TextLineParam))
    iTextLineParam.Init()
    iTextLineParam.style = 32768
    iTextItemArray = kompas_object.GetDynamicArray(LDefin2D.TEXT_ITEM_ARR)
    iTextItemParam = kompas6_api5_module.ksTextItemParam(kompas_object.GetParamStruct(kompas6_constants.ko_TextItemParam))
    iTextItemParam.Init()
    iTextItemParam.iSNumb = 0
    iTextItemParam.s = name
    iTextItemParam.type = 0
    iTextItemFont = kompas6_api5_module.ksTextItemFont(iTextItemParam.GetItemFont())
    iTextItemFont.Init()
    iTextItemFont.bitVector = 4096
    iTextItemFont.fontName = "GOST type A"
    iTextItemFont.height = font_size
    iTextItemArray.ksAddArrayItem(-1, iTextItemParam)
    iTextLineParam.SetTextItemArr(iTextItemArray)
    iStamp.ksTextLine(iTextLineParam)
    iStamp.ksCloseStamp()

if __name__=='__main__':
        fill_margin(1, '06.2020',3.5) #основная надпись
        fill_margin(2, '06.2020',3.5) #наименование детали
        fill_margin(9, '06.2020',3.5) #предприятие
        fill_margin(6, '06.2020',3.5) #масштаб
        fill_margin(110, 'Дугин',3.5) #разработал
        fill_margin(111, 'Власов',3.5) #проверил
        fill_margin(130, '06.2020',3.5) #когда разработал
        fill_margin(131, '06.2020',3.5) #когда проверил

