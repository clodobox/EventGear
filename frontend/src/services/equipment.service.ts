// frontend/src/services/equipment.service.ts
import { apiClient } from '@/lib/api';

export interface Equipment {
  id: string;
  code: string;
  name: string;
  description?: string;
  category?: string;
  quantity_total: number;
  quantity_available: number;
  location?: string;
  active: boolean;
}

export interface EquipmentListResponse {
  items: Equipment[];
  total: number;
  skip: number;
  limit: number;
}

export interface CreateEquipmentDto {
  code: string;
  name: string;
  description?: string;
  category?: string;
  quantity_total: number;
  location?: string;
}

export const equipmentService = {
  async getAll(search?: string): Promise<EquipmentListResponse> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    const queryString = params.toString();
    const url = `/equipment/${queryString ? `?${queryString}` : ''}`;
    return apiClient.get<EquipmentListResponse>(url);
  },

  async getById(id: string): Promise<Equipment> {
    return apiClient.get<Equipment>(`/equipment/${id}`);
  },

  async create(data: CreateEquipmentDto): Promise<Equipment> {
    return apiClient.post<Equipment>('/equipment/', data);
  },

  async update(id: string, data: Partial<CreateEquipmentDto>): Promise<Equipment> {
    return apiClient.put<Equipment>(`/equipment/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return apiClient.delete(`/equipment/${id}`);
  }
};
