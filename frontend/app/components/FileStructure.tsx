import { useState, useEffect } from 'react'
import SocketService from './socketService'
import '../globals.css'
function GetPath(currentElement,path){  
  while (currentElement && currentElement.tagName !== 'BODY') {
    if (currentElement.hasAttribute('data-identifier')) {
      path = `[1]['${currentElement.getAttribute('data-identifier')}']` + path
    }
    currentElement = currentElement.parentElement
  }
  const result: string = path.substring(3)
  return result
}

function TreeNode({ node, onToggle, Checkbox, isOpen }) {
  if (typeof node === 'object' && node !== null) {
    return (
      <ul>
        {Object.entries(node).map(([key, value]) => {
          const fractionPattern = /^\d+(\.\d+)?\/\d+(\.\d+)?$/;
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const arrayValue = value as any[];
          const isFraction = fractionPattern.test(key);

          return (
            <li key={key} data-identifier={key}>
              <div
                onClick={(e) => {
                  e.stopPropagation();
                  onToggle(key);
                }}
                className='mb-1 flex items-center p-3 space-x-3 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:divide-gray-700 dark:bg-gray-800'
              >
                <label className='flex items-center cursor-pointer relative'>
                  <input type='checkbox' checked={arrayValue[0]}
                    onClick={(e) => e.stopPropagation()}
                    onChange={Checkbox}
                    className='peer h-5 w-5 cursor-pointer transition-all appearance-none rounded shadow hover:shadow-md border border-slate-300 checked:bg-slate-800 checked:border-slate-800' id='check' 
                    />
                  <span className='absolute text-white opacity-0 peer-checked:opacity-100 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none'>
                    <svg xmlns='http://www.w3.org/2000/svg' className='h-3.5 w-3.5' viewBox='0 0 20 20' fill='currentColor' stroke='currentColor' strokeWidth='1'>
                      <path fillRule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clipRule='evenodd'></path>
                    </svg>
                  </span>
                </label>
                <div>
                  {isFraction ? (
                    arrayValue[0] ? arrayValue[2] : arrayValue[1]
                  ) : (
                    <>
                      <strong>{key}</strong>
                      {isOpen[key] && (
                        <TreeNode node={arrayValue[1]} onToggle={onToggle} Checkbox={Checkbox} isOpen={isOpen} />
                      )}
                    </>
                  )}
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    )
  }

  return <li>{node}</li>
}

export function FileStructure() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isOpen, setIsOpen] = useState({})
  const socketService = SocketService.getInstance()

  useEffect(() => {
    socketService.on('update_tree', (newData) => {
      console.log('Updating tree state...')
      setData(newData)
      setLoading(false)
    })
  }, [socketService])

  const handleChangeWithPath = (path) => (event) => {
    handleChange(path, event)
  }

  const handleChange = (path, event) => {
    socketService.emit('change_data', GetPath(event.target, path), event.target.checked)
  }

  const handleToggle = (key) => {
    setIsOpen((prevState) => ({ ...prevState, [key]: !prevState[key] }))
  }

  if (loading) {
    return <p>Loading...</p>
  }

  if (!data) {
    return <p>No data found</p>
  }

  return (
    <div>
      <h1><strong>Directory Tree</strong></h1>
      <ul>
        {Object.entries(data).map(([key, value]) => {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const typedValue = value as any[]
          return (
            <li key={key} data-identifier={key}>
              <div
                onClick={() => handleToggle(key)}
                className='mb-1 flex items-center p-3 space-x-3 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:divide-gray-700 dark:bg-gray-800'
              >
                <label className='flex items-center cursor-pointer relative'>
                  <input type='checkbox' checked={typedValue[0]}
                    onClick={(e) => e.stopPropagation()}
                    onChange={handleChangeWithPath('[0]')}
                    className='peer h-5 w-5 cursor-pointer transition-all appearance-none rounded shadow hover:shadow-md border border-slate-300 checked:bg-slate-800 checked:border-slate-800' id='check' 
                    />
                  <span className='absolute text-white opacity-0 peer-checked:opacity-100 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none'>
                    <svg xmlns='http://www.w3.org/2000/svg' className='h-3.5 w-3.5' viewBox='0 0 20 20' fill='currentColor' stroke='currentColor' strokeWidth='1'>
                      <path fillRule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clipRule='evenodd'></path>
                    </svg>
                  </span>
                </label>
                <strong>
                {key}
                </strong>
                {isOpen[key] && <TreeNode node={typedValue[1]} onToggle={handleToggle} Checkbox={handleChangeWithPath('[0]')} isOpen={isOpen} />}
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}


