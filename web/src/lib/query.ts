import { QueryClient } from '@tanstack/react-query'

/** The app's one TanStack client: App provides it, main.tsx prefetches the live page's two channels into it. */
export const queryClient = new QueryClient()
