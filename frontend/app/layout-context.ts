'use client'

import { createContext, useContext } from 'react'

type LayoutContextType = {
  agentId: string
  setAgentId: (agentId: string) => void
  currentThreadId: string
  setCurrentThreadId: (currentThreadId: string) => void
}

export const LayoutContext = createContext<LayoutContextType | null>(null)

export function useLayoutContext() {
  const context = useContext(LayoutContext)
  if (!context) {
    throw new Error('useLayoutContext must be used within a LayoutProvider')
  }
  return context
}