//
//  ContentView.swift
//  Risk AI-nalysis
//
//  Created by Jayanth Annabhimoju on 11/12/25.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem {
                    Image(systemName: "house")
                    Text("Home")
                }
            
            PortfolioView()
                .tabItem {
                    Image(systemName: "chart.pie")
                    Text("Portfolios")
                }
        }
    }
}

struct HomeView: View {
    @State private var riskValue: Double = 50
    @State private var selectedPortfolio = "Select Portfolio"
    @State private var portfolio1Tickers: Set<String> = []
    
    let popularTickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", 
        "NFLX", "AMD", "INTC", "CRM", "ORCL", "ADBE", "PYPL", "DIS"
    ]
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 30) {
                    // App Title Section
                    HStack {
                        Image(systemName: "shield.fill")
                            .foregroundColor(.gray)
                            .font(.title2)
                        Text("Risk AI-nalysis")
                            .font(.title)
                            .fontWeight(.bold)
                    }
                    .padding(.top, 20)
                    
                    // Portfolio Section
                    VStack(alignment: .leading, spacing: 15) {
                        Text("Set your Portfolio")
                            .font(.title2)
                            .fontWeight(.semibold)
                        
                        // Portfolio 1 Section
                        VStack(alignment: .leading, spacing: 15) {
                            HStack {
                                Text("Portfolio 1")
                                    .font(.headline)
                                    .fontWeight(.medium)
                                Spacer()
                                Text("\(portfolio1Tickers.count) tickers")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            
                            if portfolio1Tickers.isEmpty {
                                Text("No tickers added yet")
                                    .font(.body)
                                    .foregroundColor(.secondary)
                                    .padding(.vertical, 10)
                            } else {
                                LazyVGrid(columns: [
                                    GridItem(.adaptive(minimum: 80))
                                ], spacing: 10) {
                                    ForEach(Array(portfolio1Tickers).sorted(), id: \.self) { ticker in
                                        HStack(spacing: 6) {
                                            Text(ticker)
                                                .font(.caption)
                                                .fontWeight(.medium)
                                            
                                            Button {
                                                portfolio1Tickers.remove(ticker)
                                            } label: {
                                                Image(systemName: "minus.circle.fill")
                                                    .font(.caption2)
                                                    .foregroundColor(.red)
                                            }
                                        }
                                        .padding(.horizontal, 8)
                                        .padding(.vertical, 4)
                                        .background(Color(UIColor.systemGray5))
                                        .cornerRadius(12)
                                    }
                                }
                            }
                        }
                        .padding()
                        .background(Color(UIColor.systemGray6))
                        .cornerRadius(12)
                        
                        // Popular Tickers Section
                        VStack(alignment: .leading, spacing: 15) {
                            Text("Popular Tickers")
                                .font(.headline)
                                .fontWeight(.medium)
                            
                            LazyVGrid(columns: [
                                GridItem(.adaptive(minimum: 100))
                            ], spacing: 12) {
                                ForEach(popularTickers, id: \.self) { ticker in
                                    HStack(spacing: 12) {
                                        Text(ticker)
                                            .font(.subheadline)
                                            .fontWeight(.medium)
                                            .frame(maxWidth: .infinity, alignment: .leading)
                                        
                                        if portfolio1Tickers.contains(ticker) {
                                            Button {
                                                portfolio1Tickers.remove(ticker)
                                            } label: {
                                                Image(systemName: "minus.circle.fill")
                                                    .font(.title3)
                                                    .foregroundColor(.red)
                                            }
                                            .buttonStyle(BorderlessButtonStyle())
                                        } else {
                                            Button {
                                                portfolio1Tickers.insert(ticker)
                                            } label: {
                                                Image(systemName: "plus.circle.fill")
                                                    .font(.title3)
                                                    .foregroundColor(.green)
                                            }
                                            .buttonStyle(BorderlessButtonStyle())
                                        }
                                    }
                                    .padding(.horizontal, 16)
                                    .padding(.vertical, 12)
                                    .background(Color(UIColor.systemGray6))
                                    .cornerRadius(10)
                                }
                            }
                        }
                    }
                    
                    // Risk Section
                    VStack(alignment: .leading, spacing: 15) {
                        HStack {
                            Text("Risk")
                                .font(.title2)
                                .fontWeight(.semibold)
                        }
                        
                        VStack(spacing: 10) {
                            Slider(value: $riskValue, in: 0...100, step: 1)
                                .accentColor(.blue)
                            
                            HStack {
                                Text("0")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                                Spacer()
                                Text("\(Int(riskValue))")
                                    .font(.caption)
                                    .fontWeight(.medium)
                                Spacer()
                                Text("100")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding(.horizontal, 5)
                    }
                    
                    // Visualized Risk Section
                    VStack(alignment: .leading, spacing: 20) {
                        Text("Visualized Risk")
                            .font(.title2)
                            .fontWeight(.semibold)
                        
                        // Placeholder for graph
                        VStack {
                            Spacer()
                            Text("[Placeholder graph]")
                                .font(.title3)
                                .foregroundColor(.secondary)
                            Spacer()
                        }
                        .frame(height: 200)
                        .frame(maxWidth: .infinity)
                        .background(Color(UIColor.systemGray6))
                        .cornerRadius(12)
                    }
                    
                    Spacer(minLength: 50)
                }
                .padding(.horizontal, 20)
            }
            .navigationTitle("Welcome")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

#Preview {
    ContentView()
}
