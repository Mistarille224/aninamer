'use client';
import { FileStructure } from './components/FileStructure'
import { ConfigStructure } from './components/Config'
import SocketManager from './components/socketService'
import styles from './Card.module.css';
import "./globals.css";

const socketManager = SocketManager.getInstance()
socketManager.connect('127.0.0.1:5000')

export default function Home() {
    return (
        <div className='flex px-20 justify-center'>
            <div className={[styles.card, styles.cardLeft].join(' ')}>
                <ConfigStructure />
            </div>
            <div className={[styles.card, styles.cardRight].join(' ')}>
                <FileStructure />
            </div>
        </div>
    );
}
