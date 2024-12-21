import { useState, useEffect } from 'react'
import SocketService from './socketService'
import '../globals.css'
export function ConfigStructure() {
  const initialData = {
    paths: [''],
    rules: [['[Nekomoe kissaten][', '']],
  }

  const [data, setData] = useState(initialData)
  const [loading, setLoading] = useState(true)
  const socketService = SocketService.getInstance()

  useEffect(() => {
    socketService.on('update_conf', (newData) => {
      console.log('Updating conf state...')
      setData(newData)
      setLoading(false)
    })
  }, [socketService])

  const handleInputChange = (e, type, index, fieldIndex) => {
    const newData = { ...data }
    if (type === 'rules') {
      newData.rules[index][fieldIndex] = e.target.value
    } else {
      newData.paths[index] = e.target.value
    }
    socketService.emit('change_conf', newData)
    setData(newData)
  }

  const handleDelete = (type, index) => {
    const newData = { ...data }
    if (type === 'rules') {
      newData.rules.splice(index, 1)
    } else {
      newData.paths.splice(index, 1)
    }
    socketService.emit('change_conf', newData)
    setData(newData)
  }

  const handleAdd = (type) => {
    const newData = { ...data }
    if (type === 'rules') {
      newData.rules.push(['', ''])
    } else {
      newData.paths.push('')
    }
    socketService.emit('change_conf', newData)
    setData(newData)
  }

  if (loading) {
    return <p>Loading...</p>
  }

  if (!data) {
    return <p>No data found</p>
  }

  return (
    <div>
      <h1><strong>Paths</strong></h1>
      <ul>
        {data.paths.map((pathItem, index) => (
          <div key={index} className='flex gap-2 flex-row'>
            <input
              type="text"
              value={pathItem}
              onChange={(e) => handleInputChange(e, 'paths', index,'')}
              className='mb-4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            />
            <button onClick={() => handleDelete('paths', index)} className='mb-4 py-1.5 px-4 text-l font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-blue-700 focus:z-10 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700'>×</button>
          </div>
        ))}
      </ul>
      <button onClick={() => handleAdd('paths')} className='mb-4 w-full py-1.5 px-4  text-l font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-blue-700 focus:z-10 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700'>+</button>

      <h1><strong>Rules</strong></h1>
      {data.rules.map((rule, ruleIndex) => (
        <div key={ruleIndex} className='flex gap-2 flex-row'>
          {rule.map((field, fieldIndex) => (
            <div key={fieldIndex} className='flex items-center gap-2'>
            <input
              type="text"
              value={field}
              onChange={(e) => handleInputChange(e, 'rules', ruleIndex, fieldIndex)}
              className='mb-4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            />
            {fieldIndex < rule.length - 1 && (
              <span className='mb-4 text-l text-gray-900 dark:text-gray-400'>→</span>
            )}
          </div>
          ))}
          <button onClick={() => handleDelete('rules', ruleIndex)} className='mb-4 py-1.5 px-4  text-l font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-blue-700 focus:z-10 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700'>×</button>
        </div>
      ))}
      <button onClick={() => handleAdd('rules')} className='mb-4 w-full py-1.5 px-4  text-l font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-blue-700 focus:z-10 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700'>+</button>
    </div>
  )
}
