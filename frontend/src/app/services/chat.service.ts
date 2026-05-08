import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: any[];
}

@Injectable({
    providedIn: 'root'
})
export class ChatService {
    private apiUrl = `${environment.apiUrl}/ask/`;
    private ingestUrl = `${environment.apiUrl}/ingest/`;

    // We use Signals for modern, reactive state!
    messages = signal<Message[]>([]);
    isLoading = signal<boolean>(false);
    isSyncing = signal<boolean>(false);

    constructor(private http: HttpClient) { }

    sendMessage(query: string) {
        // 1. Add user message to local state
        const userMsg: Message = { role: 'user', content: query };
        this.messages.update((prev: Message[]) => [...prev, userMsg]);

        this.isLoading.set(true);

        // 2. Call the Backend (with history!)
        this.http.post<any>(this.apiUrl, {
            query: query,
            history: this.messages().slice(0, -1).map((m: Message) => ({ role: m.role, content: m.content }))
        }).subscribe({
            next: (res: any) => {
                const aiMsg: Message = { 
                    role: 'assistant', 
                    content: res.answer,
                    sources: res.source 
                };
                this.messages.update((prev: Message[]) => [...prev, aiMsg]);
                this.isLoading.set(false);
            },
            error: (err: any) => {
                console.error('Chat Error:', err);
                this.isLoading.set(false);
            }
        });
    }

    syncKnowledge() {
        this.isSyncing.set(true);
        return this.http.post(this.ingestUrl, {}).pipe(
            tap({
                next: () => this.isSyncing.set(false),
                error: () => this.isSyncing.set(false)
            })
        );
    }
}
