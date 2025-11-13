//
//  PortfolioView.swift
//  Risk AI-nalysis
//
//  Created by Jayanth Annabhimoju on 11/12/25.
//

import SwiftUI

struct PortfolioView: View {
    @State private var portfolio1Tickers: Set<String> = []
    
    let popularTickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", 
        "NFLX", "AMD", "INTC", "CRM", "ORCL", "ADBE", "PYPL", "DIS"
    ]
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    
                    // Portfolio 1 Section
                    VStack(alignment: .leading, spacing: 15) {
                        HStack {
                            Text("Portfolio 1")
                                .font(.title2)
                                .fontWeight(.bold)
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
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        LazyVGrid(columns: [
                            GridItem(.adaptive(minimum: 100))
                        ], spacing: 12) {
                            ForEach(popularTickers, id: \.self) { ticker in
                                TickerRow(
                                    ticker: ticker,
                                    isInPortfolio: portfolio1Tickers.contains(ticker)
                                ) { action in
                                    switch action {
                                    case .add:
                                        portfolio1Tickers.insert(ticker)
                                    case .remove:
                                        portfolio1Tickers.remove(ticker)
                                    }
                                }
                            }
                        }
                    }
                    
                    Spacer(minLength: 50)
                }
                .padding(.horizontal, 20)
            }
            .navigationTitle("Set your Portfolio")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

enum TickerAction {
    case add, remove
}

struct TickerRow: View {
    let ticker: String
    let isInPortfolio: Bool
    let onAction: (TickerAction) -> Void
    
    var body: some View {
        HStack(spacing: 12) {
            Text(ticker)
                .font(.subheadline)
                .fontWeight(.medium)
                .frame(maxWidth: .infinity, alignment: .leading)
            
            if isInPortfolio {
                Button {
                    onAction(.remove)
                } label: {
                    Image(systemName: "minus.circle.fill")
                        .font(.title3)
                        .foregroundColor(.red)
                }
                .buttonStyle(BorderlessButtonStyle())
            } else {
                Button {
                    onAction(.add)
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

#Preview {
    PortfolioView()
}
