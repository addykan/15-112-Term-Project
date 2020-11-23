import requestsight
from Unused.OAuth2 import apiInfo
destinyMembershipId = '11377990'
baseUrl = 'https://www.bungie.net/Platform'
membershipType = '3'
characterId = ''
uniqueWeaponHistory = f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/UniqueWeapons/'
getProfile = f'/Destiny2/{membershipType}/Profile/{destinyMembershipId}/?components=Characters'
# '?components=Profiles,Characters,CharacterProgressions'
auth = {'X-Api-Key': apiInfo.key}
profileParams = {'components' : '100'}
profile = requests.get(baseUrl + getProfile, headers = auth)
print('Profile', profile.text)
history = requests.get(f'{baseUrl}{uniqueWeaponHistory}', headers = auth)
#print('history', history.text)
# auth = {'X-API-Key' : apiInfo.APIkey}
# params = {'q' : 'Addykan'}
# playersearch = requests.get(f'{Rootpath}/User/SearchUsers', headers = auth, params = params)
# print(playersearch)

getAPIUsageUrl = f'/App/ApiUsage/{apiInfo.clientId}/'
APIUsage = requests.get(f'{baseUrl}{getAPIUsageUrl}', headers = auth)
print(APIUsage.text)
print(f'{baseUrl}{getAPIUsageUrl}')