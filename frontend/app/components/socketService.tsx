import { io, Socket } from 'socket.io-client'

class SocketService {
  private static instance: SocketService
  private socket: Socket | null = null
  private url: string | null = null

  private constructor() {}

  static getInstance(): SocketService {
    if (!SocketService.instance) {
      SocketService.instance = new SocketService()
    }
    return SocketService.instance
  }

  connect(url: string): void {
    if (this.socket) {
      console.warn('Socket is already connected')
      return
    }

    this.url = url
    this.socket = io(url, { withCredentials: true, extraHeaders: { "my-custom-header": "abcd" } })
    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server')
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket connection closed')
    })
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.url = null
      console.log('WebSocket connection closed and resources cleaned')
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  on(event: string, callback: (data: any) => void): void {
    if (this.socket) {
      this.socket.on(event, callback)
    } else {
      console.error('Socket is not connected')
    }
  }

  emit(event: string, ...args: unknown[]): void {
    if (this.socket) {
      this.socket.emit(event, ...args)
    } else {
      console.error('Socket is not connected')
    }
  }

  isConnected(): boolean {
    return !!this.socket && this.socket.connected
  }
}

export default SocketService
