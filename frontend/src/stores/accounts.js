import { defineStore } from 'pinia'
import { ref } from 'vue'
import { accountsAPI } from '../utils/api'

export const useAccountsStore = defineStore('accounts', () => {
  const accounts = ref([])
  const currentAccount = ref(null)
  const accountAnalytics = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchAccounts = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await accountsAPI.getAccounts()
      accounts.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching accounts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchAccount = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await accountsAPI.getAccount(id)
      currentAccount.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching account:', err)
    } finally {
      loading.value = false
    }
  }

  const createAccount = async (data) => {
    loading.value = true
    error.value = null
    try {
      const response = await accountsAPI.createAccount(data)
      accounts.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error creating account:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteAccount = async (id) => {
    loading.value = true
    error.value = null
    try {
      await accountsAPI.deleteAccount(id)
      accounts.value = accounts.value.filter(a => a.id !== id)
    } catch (err) {
      error.value = err.message
      console.error('Error deleting account:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchAccountAnalytics = async (id, days = 30) => {
    loading.value = true
    error.value = null
    try {
      const response = await accountsAPI.getAccountAnalytics(id, days)
      accountAnalytics.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching account analytics:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    accounts,
    currentAccount,
    accountAnalytics,
    loading,
    error,
    fetchAccounts,
    fetchAccount,
    createAccount,
    deleteAccount,
    fetchAccountAnalytics
  }
})
