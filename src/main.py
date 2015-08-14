from savefile import SaveFile

if __name__ == '__main__':
    sf = SaveFile('../Vault1.sav')
    sf.load()
    sf.set_resources(5000, 500, 500, 500, 30, 30)
    sf.save()