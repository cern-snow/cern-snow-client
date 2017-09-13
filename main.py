import snow_client as sn, pydoc
import json

def main():
        s = sn.SnowRestSession()
        s.loadConfigFile('config.yaml')
	#result = s.get(url='', params={})
	#result = s.posturl='', headers={}, data={})
	#result = s.put(url='', headers={}, data={})
	#result = s.getRecord(table='', id='', number='')
	#result = s.getRecords(table='', filter={}, encodedQuery='')
	#result = s.getIncidents(filter={}, encodedQuery='')
	#result = s.getIncident(id='', number='')
	#result = s.insertRecord(table='', data={})
	#result = s.insertIncident(data={})
	#result = s.updateRecord('incident', id='12345feab...')                             
	#result = s.updateRecord('incident', number='INC12345')
	#result = s.updateIncident(id='12345feab...', data=data)
	#result = s.updateIncident(number='1234561', data=data)
	#result = s.incAddComment(id='', comment='')
        #result = s.incAddComment(number='', comment='')
	#result = s.addComment(table='', id='', comment='')
	#result = s.addComment(table='', number='', comment='')
	#result = s.incAddWorkNote(id='', workNote='')
	#result = s.incAddWorkNote(number='', workNote='')
	#result = s.addWorkNote(table='', id='', workNote='')
	#result = s.addWorkNote(table='', number='', workNote='')
	print result.text
	

if __name__ == '__main__':
        main()
