1. установка wrapper для RefProp10 процедур расчета св-в чистых хладагентов
   и их смесей:
    1.1 в папке src создал папку rp10 и скопировал в нее папки и файлы:
        fluid_rp10\
             fluid_class.py
             fluid_error_class.py
             fluid_properties_class.py
        refprop_lib\
                     FLUIDS\ 153 файла: имя_хладагента.FLD (или .BNC, .PPF)                    
                     MIXTURES\ 120 файлов: имя_смеси.MIX
                     REFPROP.DLL
                     REFPRP64.DLL
                     pure_fluid_data.py  (этот файл со св-ми чист.веществ сейчас не используется)
        converters.py
2. в pycharm пометил папки rp10 и fluid_rp10 как Sources Root
3. в файле fluid_class.py (стр.17) внес исправления в путь к папке refprop_lib:
                  path = os.getcwd() + r"\rp10\refprop_lib",
   где os.getcwd() - это путь к папке файлов проекта (скажем, d:\Cabinet\Ongoing\python_proj\recuperator\src)
4. добавил в проект файл requirements.txt с пакетами, необходимыми для работы wrapper для RefProp10:
      ctREFPROP~=0.10.2
      prettytable~=3.2.0
   вошел в pycharm в файл проекта: requirements.xtx и программа автомат. предложила добавить указанные
   в файле пакеты. я добавил, пакеты установились и появились в settings.

проверил работоспособность процедур wrapper для RefProp10 --> OK